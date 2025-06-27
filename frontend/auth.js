document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login');
  const registerForm = document.getElementById('register');
  const guestLoginBtn = document.getElementById('guest-login');
  const showRegisterBtn = document.getElementById('show-register');
  const showLoginBtn = document.getElementById('show-login');
  const loginDiv = document.getElementById('login-form');
  const registerDiv = document.getElementById('register-form');
  const container = document.querySelector('.container');
  const cookies = document.querySelector('.cookies');
  const errorElement = document.querySelector('.error');

  function showError(message) {
    errorElement.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="error-svg" viewBox="0 0 24 24">
        <path fill="currentColor" d="M12.5 8.752a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0Z"/>
        <circle cx="11.999" cy="16.736" r=".5" fill="currentColor" />
        <path fill="currentColor" d="M18.642 20.934H5.385a2.5 2.5 0 0 1-2.222-3.644L9.792 4.421a2.5 2.5 0 0 1 4.444 0l6.629 12.869a2.5 2.5 0 0 1-2.223 3.644"/>
      </svg>
      ERROR! ${message}`;
    errorElement.style.display = 'flex';
    setTimeout(() => (errorElement.style.display = 'none'), 5000);
  }

  function saveToken(token) {
    localStorage.setItem('videoscop_token', token);
    const rememberMe = document.getElementById('remember-me').checked;
    if (rememberMe) {
      sessionStorage.setItem('videoscop_token', token);
    }
  }

  async function loginUser(login, password) {
    const res = await fetch('http://217.114.10.197:8000/users/me/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ login, password }),
    });

    const data = await res.json();
    if (!res.ok || !data.token) {
      throw new Error(data.detail || 'Ошибка авторизации');
    }

    saveToken(data.token); 
    window.location.href = 'home.html';
    console.log(data.token);
  }

  document.getElementById('agree-with-cookies').addEventListener('click', () => {
    cookies.classList.remove('clicked');
    container.style.opacity = '1';
    document.querySelectorAll('button, input').forEach(el => el.disabled = false);
  });

  showRegisterBtn.addEventListener('click', () => {
    loginDiv.style.display = 'none';
    registerDiv.style.display = 'block';
    errorElement.style.display = 'none';
  });

  showLoginBtn.addEventListener('click', () => {
    registerDiv.style.display = 'none';
    loginDiv.style.display = 'block';
    errorElement.style.display = 'none';
  });

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!document.getElementById('login-agree').checked) {
      return showError('с политикой надо согласиться');
    }

    const login = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();

    if (!login || !password) {
      return showError('не все заполнено братан');
    }

    try {
      await loginUser(login, password);
    } catch (err) {
      showError(err.message);
    }
  });

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!document.getElementById('register-agree').checked) {
      return showError('с политикой надо согласиться');
    }

    const login = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value.trim();

    if (!login || !email || !password) {
      return showError('все поля обязательны');
    }

    try {
      const res = await fetch('http://217.114.10.197:8000/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, email, password }),
      });

      const errData = await res.json();
      if (!res.ok) {
        const errorMessage = errData.message || 'Ошибка регистрации';
        throw new Error(errorMessage);
      }

      await loginUser(login, password);
    } catch (err) {
      showError(err.message);
    }
  });

  guestLoginBtn.addEventListener('click', () => {
    if (!document.getElementById('login-agree').checked) {
      cookies.style.display = 'flex';
      return;
    }

    sessionStorage.setItem('videoscop_guest', 'true');
    localStorage.removeItem('videoscop_token');
    sessionStorage.removeItem('videoscop_token');
    window.location.href = 'home.html';
  });

  (function checkAuth() {
    const token = localStorage.getItem('videoscop_token') || sessionStorage.getItem('videoscop_token');
  })();
});
