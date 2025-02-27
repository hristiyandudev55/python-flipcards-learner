<script setup>
const baseUrl = import.meta.env.VITE_S3_BASE_URL;
</script>

<template>
  <img :src="`${baseUrl}/githubactions.png`" alt="Github Actions Icon" width="32" height="32" />
</template>