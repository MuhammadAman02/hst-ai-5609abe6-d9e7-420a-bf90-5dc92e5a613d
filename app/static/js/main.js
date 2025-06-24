// Swiss Luxury Timepieces - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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
    
    // Image Lazy Loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Product Image Gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainImage');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            if (mainImage) {
                mainImage.src = this.src;
                
                // Update active thumbnail
                thumbnails.forEach(thumb => thumb.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    showFieldError(field, 'This field is required');
                } else {
                    field.classList.remove('error');
                    hideFieldError(field);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    // Search Functionality
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
    }
    
    // Cart Functionality
    initializeCart();
    
    // Scroll to Top Button
    const scrollTopBtn = createScrollTopButton();
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('show');
        } else {
            scrollTopBtn.classList.remove('show');
        }
    });
});

// Cart Functions
function initializeCart() {
    updateCartCount();
    
    // Add to cart buttons
    document.querySelectorAll('[data-add-to-cart]').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
}

async function addToCart(productId) {
    try {
        showLoading();
        
        const response = await fetch(`/cart/add/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        hideLoading();
        
        if (response.ok) {
            showNotification('Product added to cart successfully!', 'success');
            updateCartCount();
            
            // Add visual feedback
            const button = document.querySelector(`[data-product-id="${productId}"]`);
            if (button) {
                button.classList.add('added');
                button.textContent = 'Added!';
                setTimeout(() => {
                    button.classList.remove('added');
                    button.textContent = 'Add to Cart';
                }, 2000);
            }
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Failed to add product to cart', 'error');
        }
    } catch (error) {
        hideLoading();
        showNotification('An error occurred. Please try again.', 'error');
        console.error('Cart error:', error);
    }
}

async function removeFromCart(productId) {
    try {
        showLoading();
        
        const response = await fetch(`/cart/remove/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        hideLoading();
        
        if (response.ok) {
            showNotification('Product removed from cart', 'success');
            // Reload page to update cart display
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Failed to remove product from cart', 'error');
        }
    } catch (error) {
        hideLoading();
        showNotification('An error occurred', 'error');
        console.error('Cart error:', error);
    }
}

async function updateCartCount() {
    try {
        const response = await fetch('/api/cart/count');
        if (response.ok) {
            const data = await response.json();
            const cartCountElements = document.querySelectorAll('.cart-count');
            cartCountElements.forEach(element => {
                element.textContent = data.count;
                element.style.display = data.count > 0 ? 'inline' : 'none';
            });
        }
    } catch (error) {
        console.error('Failed to update cart count:', error);
    }
}

// Search Functions
async function performSearch(query) {
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        if (response.ok) {
            const results = await response.json();
            displaySearchResults(results);
        }
    } catch (error) {
        console.error('Search error:', error);
    }
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-no-results">No products found</div>';
    } else {
        searchResults.innerHTML = results.map(product => `
            <div class="search-result-item">
                <img src="${product.image_url}" alt="${product.name}" class="search-result-image">
                <div class="search-result-info">
                    <h4>${product.name}</h4>
                    <p>${product.collection}</p>
                    <span class="search-result-price">$${product.price.toLocaleString()}</span>
                </div>
            </div>
        `).join('');
    }
    
    searchResults.style.display = 'block';
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 4000);
    
    // Click to dismiss
    notification.addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    });
}

// Loading Indicator
function showLoading() {
    let loader = document.getElementById('global-loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'global-loader';
        loader.className = 'loading-overlay';
        loader.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
        `;
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

function hideLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Form Validation Helpers
function showFieldError(field, message) {
    hideFieldError(field);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    
    field.parentNode.appendChild(errorElement);
    field.classList.add('error');
}

function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.classList.remove('error');
}

// Scroll to Top Button
function createScrollTopButton() {
    const button = document.createElement('button');
    button.className = 'scroll-top-btn';
    button.innerHTML = '↑';
    button.setAttribute('aria-label', 'Scroll to top');
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    return button;
}

// Product Filter Functions
function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    const filterTabs = document.querySelectorAll('.filter-tab');
    
    // Update active tab
    filterTabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.category === category) {
            tab.classList.add('active');
        }
    });
    
    // Filter products
    products.forEach(product => {
        if (category === 'all' || product.dataset.category === category) {
            product.style.display = 'block';
            product.classList.add('fade-in');
        } else {
            product.style.display = 'none';
            product.classList.remove('fade-in');
        }
    });
}

// Price Formatting
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// Image Error Handling
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        e.target.src = '/static/images/placeholder-watch.jpg';
        e.target.alt = 'Image not available';
    }
}, true);

// Performance Monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }
        }, 0);
    });
}

// Accessibility Improvements
document.addEventListener('keydown', function(e) {
    // Escape key closes modals and dropdowns
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            closeModal(activeModal);
        }
        
        const activeDropdown = document.querySelector('.dropdown.active');
        if (activeDropdown) {
            activeDropdown.classList.remove('active');
        }
    }
});

// Focus management for better accessibility
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

// Export functions for use in templates
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.showNotification = showNotification;
window.filterProducts = filterProducts;