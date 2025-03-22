<template>
  <nav mt-6 flex gap-4 justify-center text-xl>
    <button icon-btn @click="toggleDark()">
      <div i-carbon-sun dark:i-carbon-moon />
    </button>

    <a
      i-carbon-logo-github icon-btn
      rel="noreferrer"
      href="https://github.com/gaojunran/sleepy"
      target="_blank"
      title="GitHub"
    />
  </nav>
</template>
