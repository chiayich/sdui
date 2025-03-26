<template>
  <div class="home">
    <h1>SDUI Framework Demo</h1>
    
    <section class="intro">
      <h2>服务器驱动UI框架</h2>
      <p>
        SDUI (Server-Driven UI) 是一种由服务端控制UI展示的架构模式。
      </p>
    </section>
    
    <section class="demo-links">
      <h2>示例屏幕</h2>
      <div class="card-container">
        <div class="card" @click="navigateToScreen('home')">
          <h3>首页示例</h3>
          <p>展示基本容器、文本和按钮组件</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    navigateToScreen(screenId) {
      this.$router.push(`/sdui/${screenId}`);
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
}

.intro {
  max-width: 800px;
  margin: 0 auto 2rem;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.card {
  width: 250px;
  padding: 1.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card h3 {
  margin-top: 0;
  color: #336699;
}
</style> 