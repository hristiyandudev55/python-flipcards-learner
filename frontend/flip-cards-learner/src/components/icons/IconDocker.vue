<script setup>
const baseUrl = import.meta.env.VITE_S3_BASE_URL;
</script>

<template>
  <img :src="`${baseUrl}/docker.png`" alt="Docker Icon" width="32" height="32" />
</template>