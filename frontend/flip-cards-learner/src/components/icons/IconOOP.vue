<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('Python.png')" alt="OOP Icon" width="32" height="32" />
</template>