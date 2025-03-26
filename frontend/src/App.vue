<template>
  <header>
    <div class="app-header">
      <h1>SDUI Framework</h1>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/sdui/home">SDUI Demo</router-link> |
        <router-link to="/logs">Logs</router-link> |
        <router-link to="/about">About</router-link>
      </nav>
    </div>
  </header>

  <main>
    <router-view />
  </main>

  <footer>
    <p>SDUI Framework - Server-Driven UI</p>
  </footer>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  color: #333;
  line-height: 1.6;
}

.app-header {
  background-color: #336699;
  color: white;
  padding: 1rem;
  text-align: center;
}

.app-header h1 {
  margin: 0 0 1rem 0;
}

.app-header nav {
  margin-bottom: 0.5rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
  margin: 0 0.5rem;
}

.app-header nav a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

footer {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
  margin-top: 2rem;
}
</style> 