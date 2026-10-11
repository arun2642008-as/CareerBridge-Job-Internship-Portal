// ========================================
// CareerBridge - Main JavaScript
// ========================================

document.addEventListener("DOMContentLoaded", () => {
    initializeNavigation();
    initializeScrollEffects();
});


// ========================================
// Navigation
// ========================================

function initializeNavigation() {
    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const target = link.getAttribute("href");

            if (!target || !target.startsWith("#")) {
                return;
            }

            const section = document.querySelector(target);

            if (!section) {
                return;
            }

            event.preventDefault();

            section.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    });
}


// ========================================
// Scroll Effects
// ========================================

function initializeScrollEffects() {
    const navbar = document.querySelector(".navbar");

    if (!navbar) {
        return;
    }

    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.classList.add("navbar-scrolled");
        } else {
            navbar.classList.remove("navbar-scrolled");
        }
    });
}


// ========================================
// API Helper
// ========================================

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = {
            success: false,
            message: "Invalid server response"
        };
    }

    if (!response.ok) {
        throw new Error(
            data.message || "Something went wrong"
        );
    }

    return data;
}


// ========================================
// Session Helper
// ========================================

async function getCurrentUser() {
    try {
        return await apiRequest(
            "http://127.0.0.1:5000/api/auth/me",
            {
                method: "GET"
            }
        );
    } catch {
        return null;
    }
}


// ========================================
// Logout Helper
// ========================================

async function logoutUser() {
    try {
        await apiRequest(
            "http://127.0.0.1:5000/api/auth/logout",
            {
                method: "POST"
            }
        );

        window.location.href = "index.html";

    } catch (error) {
        console.error("Logout failed:", error);
    }
}