<script setup lang="ts">



</script>

<template>
  <div>
    <h1 class="font-bold text-5xl gradient-yellow inline-block">我在干嘛?</h1>
    <div flex gap-5 text-3xl mt-8 justify-center>
      <div font-bold text-white:50>手机</div>
      <div font-bold>Bilibili</div>
    </div>
    <div flex gap-5 text-3xl my-4 justify-center>
      <div font-bold text-white:50>电脑</div>
      <div font-bold>VS Code</div>
    </div>
  </div>
</template>


<style scoped>
.gradient-yellow {
  background: linear-gradient(to right, #d9ab42, #fad689);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
</style>
