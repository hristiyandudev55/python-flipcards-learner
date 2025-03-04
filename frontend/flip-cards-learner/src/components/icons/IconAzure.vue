<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('Azure.png')" alt="Azure Icon" width="32" height="32" />
</template>