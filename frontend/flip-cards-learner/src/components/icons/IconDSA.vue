<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('algorithms.png')" alt="DSA Icon" width="32" height="32" />
</template>