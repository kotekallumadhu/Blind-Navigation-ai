// Common JavaScript for Blind Navigation AI

// Theme toggle
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    body.dataset.theme = body.dataset.theme === 'dark' ? 'light' : 'dark';
    themeToggle.textContent = body.dataset.theme === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', body.dataset.theme);
});

// Load theme from localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.dataset.theme = savedTheme;
    themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
}