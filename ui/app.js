// Main application logic
let ws = null;
let currentTaskId = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    setupEventListeners();
    checkApiHealth();
});

// WebSocket connection
function initializeWebSocket() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        updateConnectionStatus(true);
    };
    
    ws.onclose = () => {
        updateConnectionStatus(false);
        // Attempt reconnect after 5 seconds
        setTimeout(initializeWebSocket, 5000);
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateConnectionStatus(false);
    };
}

function updateConnectionStatus(connected) {
    const indicator = document.getElementById('connection-status');
    const text = document.getElementById('status-text');
    
    if (connected) {
        indicator.style.color = '#10b981';
        text.textContent = 'Connected';
    } else {
        indicator.style.color = '#ef4444';
        text.textContent = 'Disconnected';
    }
}

function handleWebSocketMessage(data) {
    if (data.type === 'task_update') {
        handleTaskUpdate(data);
    }
}

// Event listeners
function setupEventListeners() {
    // Send button
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    
    sendBtn.addEventListener('click', () => sendMessage());
    
    // Enter to send (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Example prompts
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const prompt = btn.getAttribute('data-prompt');
            userInput.value = prompt;
            sendMessage();
        });
    });
    
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            switchTab(tab.getAttribute('data-tab'));
        });
    });
}

// Send message
async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input
    userInput.disabled = true;
    document.getElementById('send-btn').disabled = true;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input
    userInput.value = '';
    
    // Add processing indicator
    addMessage('system', 'Processing task... The agents are collaborating on your request.', true);
    
    try {
        // Send to API
        const response = await fetch('/api/task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message }),
        });
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // Poll for results
        pollTaskStatus(data.task_id);
        
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('error', 'Failed to send message. Please try again.');
        userInput.disabled = false;
        document.getElementById('send-btn').disabled = false;
    }
}

// Poll task status
async function pollTaskStatus(taskId) {
    const maxAttempts = 120; // 2 minutes max
    let attempts = 0;
    
    const poll = async () => {
        try {
            const response = await fetch(`/api/task/${taskId}`);
            const task = await response.json();
            
            if (task.status === 'completed') {
                handleTaskComplete(task);
                return;
            } else if (task.status === 'failed') {
                handleTaskFailed(task);
                return;
            }
            
            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(poll, 1000);
            } else {
                addMessage('error', 'Task timed out. Please try again.');
                resetInput();
            }
        } catch (error) {
            console.error('Error polling task:', error);
            addMessage('error', 'Error checking task status.');
            resetInput();
        }
    };
    
    poll();
}

function handleTaskComplete(task) {
    // Remove processing indicator
    const messages = document.getElementById('messages');
    const lastMessage = messages.lastElementChild;
    if (lastMessage && lastMessage.classList.contains('processing')) {
        lastMessage.remove();
    }
    
    // Add result
    const result = task.result.final_output;
    addMessage('assistant', result);
    
    // Update execution log
    updateExecutionLog(task.result.logs || []);
    
    // Update plan view
    updatePlanView(task.result.plan || {});
    
    // Re-enable input
    resetInput();
}

function handleTaskFailed(task) {
    addMessage('error', `Task failed: ${task.error || 'Unknown error'}`);
    resetInput();
}

function handleTaskUpdate(data) {
    // Update agent status
    if (data.agent) {
        updateAgentStatus(data.agent, data.status);
    }
}

function resetInput() {
    document.getElementById('user-input').disabled = false;
    document.getElementById('send-btn').disabled = false;
    currentTaskId = null;
}

// UI Updates
function addMessage(type, content, processing = false) {
    const messages = document.getElementById('messages');
    
    // Remove welcome message if present
    const welcome = messages.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    if (processing) messageDiv.classList.add('processing');
    
    const icon = {
        'user': '👤',
        'assistant': '🤖',
        'system': '⚙️',
        'error': '❌'
    }[type] || '•';
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span>${icon}</span>
            <span>${type.charAt(0).toUpperCase() + type.slice(1)}</span>
            ${processing ? '<span class="loading"></span>' : ''}
        </div>
        <div class="message-content">${formatContent(content)}</div>
    `;
    
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function formatContent(content) {
    // Simple markdown-like formatting
    content = content.replace(/\n/g, '<br>');
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
    content = content.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Format URLs
    content = content.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Format headers
    content = content.replace(/^# (.*?)$/gm, '<h3>$1</h3>');
    content = content.replace(/^## (.*?)$/gm, '<h4>$1</h4>');
    
    return content;
}

function updateAgentStatus(agent, status) {
    const agentCard = document.querySelector(`[data-agent="${agent}"]`);
    if (agentCard) {
        const statusEl = agentCard.querySelector('.agent-status');
        statusEl.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        
        agentCard.classList.add('active');
        setTimeout(() => {
            agentCard.classList.remove('active');
        }, 2000);
    }
}

function updateExecutionLog(logs) {
    const logEl = document.getElementById('execution-log');
    logEl.innerHTML = '';
    
    if (logs.length === 0) {
        logEl.innerHTML = '<p class="empty-state">No execution log yet</p>';
        return;
    }
    
    logs.forEach((entry, i) => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry step';
        logEntry.innerHTML = `
            <strong>Step ${entry.step_id}: ${entry.agent}</strong><br>
            <span class="log-time">${entry.action}</span><br>
            <div style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.8;">
                ${entry.output ? entry.output.substring(0, 100) + '...' : 'No output'}
            </div>
        `;
        logEl.appendChild(logEntry);
    });
}

function updatePlanView(plan) {
    const planEl = document.getElementById('plan-view');
    planEl.innerHTML = '';
    
    if (!plan.steps || plan.steps.length === 0) {
        planEl.innerHTML = '<p class="empty-state">No plan yet</p>';
        return;
    }
    
    if (plan.rationale) {
        const rationale = document.createElement('div');
        rationale.style.cssText = 'margin-bottom: 1rem; padding: 0.75rem; background: var(--bg-lighter); border-radius: 6px;';
        rationale.innerHTML = `<strong>Rationale:</strong> ${plan.rationale}`;
        planEl.appendChild(rationale);
    }
    
    plan.steps.forEach(step => {
        const stepEl = document.createElement('div');
        stepEl.className = 'plan-step';
        stepEl.innerHTML = `
            <div>
                <span class="step-number">${step.id}</span>
                <strong>${step.agent}</strong>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.85rem;">
                ${step.action}
            </div>
            ${step.dependencies && step.dependencies.length > 0 ? 
                `<div style="margin-top: 0.5rem; font-size: 0.75rem; color: var(--text-dim);">
                    Depends on: Step ${step.dependencies.join(', Step ')}
                </div>` : ''}
        `;
        planEl.appendChild(stepEl);
    });
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

// Health check
async function checkApiHealth() {
    try {
        const response = await fetch('/api/agents/status');
        const data = await response.json();
        console.log('Agents status:', data);
    } catch (error) {
        console.error('API health check failed:', error);
    }
}

