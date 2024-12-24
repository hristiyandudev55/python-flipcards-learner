<!-- filepath: /Users/a516095/Documents/GitHub/flip-cards/python-flipcards-learner/frontend/flip-cards-learner/src/views/CardsView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const category = route.params.category.toUpperCase()

const cards = ref([])
const error = ref(null)
const isFlipped = ref(false)

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/cards/${category}`)
        cards.value = response.data
    } catch (err) {
        console.error('Error:', err)
        error.value = err.response?.data?.detail || 'Error fetching cards'
    }
})

const currentIndex = ref(0)
const currentCard = computed(() => cards.value[currentIndex.value])

const nextCard = () => {
    if (currentIndex.value < cards.value.length - 1) {
        currentIndex.value++
        isFlipped.value = false
    }
}

const previousCard = () => {
    if (currentIndex.value > 0) {
        currentIndex.value--
        isFlipped.value = false
    }
}

const flipCard = () => {
    isFlipped.value = !isFlipped.value
}

const goBack = () => {
  router.push('/category')
}
</script>

<template>
  <div class="cards-view">
    <button class="back-button" @click="goBack">← Back</button>
    <h1>{{ category }} Cards</h1>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-if="cards.length" class="card-container">
        <div class="flip-card" :class="{ 'is-flipped': isFlipped }" @click="flipCard">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <p>{{ currentCard.front_text }}</p>
            </div>
            <div class="flip-card-back">
              <p>{{ currentCard.back_text }}</p>
            </div>
          </div>
        </div>
        <div class="navigation">
          <button @click.stop="previousCard" :disabled="currentIndex === 0">Previous</button>
          <button @click.stop="nextCard" :disabled="currentIndex === cards.length - 1">Next</button>
        </div>
      </div>
      <div v-else>No cards available</div>
    </div>
  </div>
</template>

<style scoped>
.cards-view {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.flip-card {
  width: 600px;
  height: 400px;
  perspective: 1000px;
  cursor: pointer;
  margin: 20px auto;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.is-flipped .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  border-radius: 8px;
  font-size: 1.2em;
  line-height: 1.6;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  font-weight: bold;
  border: none;
}

.flip-card-back {
  transform: rotateY(180deg);
}

.navigation {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.error {
  color: red;
  text-align: center;
  margin: 20px;
}

button {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  cursor: pointer;
  font-size: 1.1em;
  transition: all 0.3s ease;
}

button:hover {
  background-color: hsla(160, 100%, 37%, 0.8);
}

button:disabled {
  background-color: #ccc;
  color: #666;  
  cursor: not-allowed;
}

h1 {
  color: hsla(160, 100%, 37%, 1);
  margin-bottom: 40px;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  cursor: pointer;
  font-size: 1.1em;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: hsla(160, 100%, 37%, 0.8);
}
</style>