// Enhanced Emotion Detection Web App JavaScript

console.log("🎯 Emotion Detection Web App Initialized");

// Global variables
let isFullscreen = false;
let refreshInterval;

// Initialize the application
function initialize() {
    console.log("🚀 Starting application initialization...");
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize video monitoring
    initializeVideoMonitoring();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Add performance monitoring
    monitorPerformance();
    
    // Add interactive elements
    addInteractiveElements();
    
    console.log("✅ Application initialized successfully!");
}

// Add smooth scrolling to navigation links
function addSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active nav link
                navLinks.forEach(nav => nav.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

// Initialize video feed monitoring
function initializeVideoMonitoring() {
    const videoFeed = document.querySelector('.video-feed');
    const statusDot = document.querySelector('.status-dot');
    
    if (!videoFeed || !statusDot) {
        console.warn("⚠️ Video elements not found");
        return;
    }
    
    // Monitor video feed status
    videoFeed.addEventListener('load', () => {
        console.log("📹 Video feed loaded successfully");
        statusDot.classList.add('active');
    });
    
    videoFeed.addEventListener('error', () => {
        console.error("❌ Video feed error");
        statusDot.classList.remove('active');
        showNotification("Video feed error. Please check your camera.", 'error');
    });
    
    // Auto-refresh video feed every 30 seconds
    refreshInterval = setInterval(() => {
        refreshVideoFeed();
    }, 30000);
}

// Refresh video feed
function refreshFeed() {
    console.log("🔄 Refreshing video feed...");
    const videoFeed = document.querySelector('.video-feed');
    
    if (videoFeed) {
        // Add loading state
        const loadingOverlay = createLoadingOverlay();
        videoFeed.parentElement.appendChild(loadingOverlay);
        
        // Refresh the feed
        const currentSrc = videoFeed.src;
        videoFeed.src = '';
        
        setTimeout(() => {
            videoFeed.src = currentSrc + '?t=' + new Date().getTime();
            
            // Remove loading overlay after 2 seconds
            setTimeout(() => {
                if (loadingOverlay.parentElement) {
                    loadingOverlay.parentElement.removeChild(loadingOverlay);
                }
            }, 2000);
        }, 100);
        
        showNotification("Video feed refreshed!", 'success');
    }
}

// Create loading overlay
function createLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="loading"></div>
            <p>Refreshing feed...</p>
        </div>
    `;
    
    overlay.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
        border-radius: 15px;
    `;
    
    const loadingContent = overlay.querySelector('.loading-content');
    loadingContent.style.cssText = `
        text-align: center;
        color: white;
        font-weight: 500;
    `;
    
    return overlay;
}

// Toggle fullscreen mode
function toggleFullscreen() {
    const videoWrapper = document.querySelector('.video-wrapper');
    
    if (!videoWrapper) {
        console.warn("⚠️ Video wrapper not found");
        return;
    }
    
    if (!isFullscreen) {
        // Enter fullscreen
        if (videoWrapper.requestFullscreen) {
            videoWrapper.requestFullscreen();
        } else if (videoWrapper.webkitRequestFullscreen) {
            videoWrapper.webkitRequestFullscreen();
        } else if (videoWrapper.msRequestFullscreen) {
            videoWrapper.msRequestFullscreen();
        }
        
        isFullscreen = true;
        console.log("🖥️ Entered fullscreen mode");
        showNotification("Fullscreen mode activated", 'info');
    } else {
        // Exit fullscreen
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        
        isFullscreen = false;
        console.log("🖥️ Exited fullscreen mode");
        showNotification("Fullscreen mode deactivated", 'info');
    }
}

// Add keyboard shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // F11 - Toggle fullscreen
        if (e.key === 'F11') {
            e.preventDefault();
            toggleFullscreen();
        }
        
        // F5 or Ctrl+R - Refresh feed
        if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
            e.preventDefault();
            refreshFeed();
        }
        
        // Escape - Exit fullscreen
        if (e.key === 'Escape' && isFullscreen) {
            toggleFullscreen();
        }
    });
}

// Monitor performance
function monitorPerformance() {
    // Log performance metrics
    if (window.performance && window.performance.timing) {
        window.addEventListener('load', () => {
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            console.log(`⚡ Page loaded in ${loadTime}ms`);
        });
    }
    
    // Monitor video feed performance
    const videoFeed = document.querySelector('.video-feed');
    if (videoFeed) {
        let frameCount = 0;
        const startTime = Date.now();
        
        setInterval(() => {
            frameCount++;
            const elapsed = Date.now() - startTime;
            const fps = Math.round((frameCount / elapsed) * 1000);
            
            // Log FPS every 10 seconds
            if (frameCount % 10 === 0) {
                console.log(`📊 Estimated FPS: ${fps}`);
            }
        }, 1000);
    }
}

// Add interactive elements
function addInteractiveElements() {
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click animations to buttons
    const buttons = document.querySelectorAll('.control-btn');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            
            button.style.position = 'relative';
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
}