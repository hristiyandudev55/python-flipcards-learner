<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('HTML5.png')" alt="HTML5 Icon" width="32" height="32" />
</template>