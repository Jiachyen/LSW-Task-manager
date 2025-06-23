// LSW Task Manager JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Form validation - only for specific forms, not login
    const forms = document.querySelectorAll('form:not(.login-form)');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showMessage('Please fill in all required fields.', 'error');
            }
        });
    });

    // Task completion confirmation
    const completeButtons = document.querySelectorAll('.btn-success');
    completeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const taskName = this.closest('.task-card').querySelector('h3').textContent;
            if (!confirm(`Are you sure you want to mark "${taskName}" as completed?`)) {
                e.preventDefault();
            }
        });
    });

    // Task uncompletion confirmation
    const uncompleteButtons = document.querySelectorAll('.btn-warning');
    uncompleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const taskName = this.closest('.task-card').querySelector('h3').textContent;
            if (!confirm(`Are you sure you want to mark "${taskName}" as incomplete?`)) {
                e.preventDefault();
            }
        });
    });

    // Task deletion confirmation
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const taskName = this.closest('.task-card').querySelector('h3').textContent;
            if (!confirm(`Are you sure you want to DELETE "${taskName}"? This action cannot be undone.`)) {
                e.preventDefault();
            }
        });
    });

    // Task assignment confirmation
    const assignForm = document.querySelector('.assign-form');
    if (assignForm) {
        assignForm.addEventListener('submit', function(e) {
            const taskName = this.querySelector('#task_name').value;
            const assignedTo = this.querySelector('#assigned_to').value;
            
            if (taskName && assignedTo) {
                const confirmMessage = `Assign task "${taskName}" to ${assignedTo}?`;
                if (!confirm(confirmMessage)) {
                    e.preventDefault();
                }
            }
        });
    }

    // Add own task confirmation
    const addOwnTaskForm = document.querySelector('.add-task-form');
    if (addOwnTaskForm) {
        addOwnTaskForm.addEventListener('submit', function(e) {
            const taskName = this.querySelector('#task_name').value;
            if (taskName) {
                const confirmMessage = `Add task "${taskName}" to your list?`;
                if (!confirm(confirmMessage)) {
                    e.preventDefault();
                }
            }
        });
    }

    // Progress bar animation
    const progressBars = document.querySelectorAll('.completion-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });

    // Task card hover effects
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        });
    });

    // Search functionality for tasks (if needed)
    const searchInput = document.querySelector('#search-tasks');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const taskCards = document.querySelectorAll('.task-card');
            
            taskCards.forEach(card => {
                const taskName = card.querySelector('h3').textContent.toLowerCase();
                if (taskName.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Auto-refresh for overview page (every 30 seconds)
    if (window.location.pathname === '/overview') {
        setInterval(() => {
            window.location.reload();
        }, 30000);
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                activeForm.submit();
            }
        }

        // Escape to close alerts
        if (e.key === 'Escape') {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => alert.remove());
        }
    });

    // Show message function
    function showMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => {
                alertDiv.remove();
            }, 300);
        }, 3000);
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize tooltips (if any)
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
});

// Add CSS for tooltips
const tooltipCSS = `
.tooltip {
    position: absolute;
    background: #000000;
    color: #FFD700;
    padding: 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    z-index: 1000;
    pointer-events: none;
}

.tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #000000 transparent transparent transparent;
}

.form-control.error {
    border-color: #000000;
    box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.3);
}
`;

// Inject tooltip CSS
const style = document.createElement('style');
style.textContent = tooltipCSS;
document.head.appendChild(style); 