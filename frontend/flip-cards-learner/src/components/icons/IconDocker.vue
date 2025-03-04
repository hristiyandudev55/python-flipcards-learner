<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('docker.png')" alt="Docker Icon" width="32" height="32" />
</template>