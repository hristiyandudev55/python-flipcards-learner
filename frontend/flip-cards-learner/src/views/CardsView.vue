<!-- filepath: /Users/a516095/Documents/GitHub/flip-cards/python-flipcards-learner/frontend/flip-cards-learner/src/views/CardsView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import IconOOP from '../components/icons/IconOOP.vue'
import IconDSA from '../components/icons/IconDSA.vue'
import IconHTML from '../components/icons/IconHTML.vue'
import IconDocker from '../components/icons/IconDocker.vue'
import IconGitHubAction from '../components/icons/IconGitHubAction.vue'
import IconAzure from '../components/icons/IconAzure.vue'
import IconLinux from '../components/icons/IconLinux.vue'


const route = useRoute()
const router = useRouter()
const category = route.params.category.toUpperCase()

const cards = ref([])
const error = ref(null)
const isFlipped = ref(false)

const categoryIcons = {
  OOP: IconOOP,
  DSA: IconDSA,
  WEB: IconHTML,
  DOCKER: IconDocker,
  CI_CD: IconGitHubAction,
  AZURE: IconAzure,
  LINUX: IconLinux
}

const currentIcon = computed(() => categoryIcons[category])

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
    <div class="category-header">
      <component :is="currentIcon" class="category-icon" v-if="currentIcon"/>
      <h1>{{ category }} Cards</h1>
    </div>
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
.category-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: 48px;
}

.category-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  color: hsla(160, 100%, 37%, 1);
}

h1 {
  margin: 0;
  font-size: 2.5em;
  font-weight: 600;
  color: hsla(160, 100%, 37%, 1);
  white-space: nowrap;
  line-height: 48px;
  display: flex;
  align-items: center;
}

.cards-view {
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
  width: 100%;
  margin: 0;
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.flip-card {
  width: 650px;
  height: 400px;
  perspective: 1500px;
  cursor: pointer;
  margin: 20px auto;
  filter: drop-shadow(0 0 15px rgba(0, 0, 0, 0.3));
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
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
  padding: 2.5rem;
  border-radius: 12px;
  font-size: 1.3em;
  line-height: 1.6;
  background: linear-gradient(135deg, hsla(160, 100%, 37%, 1), hsla(160, 100%, 30%, 1));
  color: white;
  font-weight: 500;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.flip-card-front::before,
.flip-card-back::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
  pointer-events: none;
}

.flip-card-back {
  transform: rotateY(180deg);
}

.navigation {
  display: flex;
  gap: 1.5rem;
  margin-top: 2rem;
}

button {
  padding: 0.8rem 1.8rem;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, hsla(160, 100%, 37%, 1), hsla(160, 100%, 30%, 1));
  color: white;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-transform: uppercase;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, hsla(160, 100%, 40%, 1), hsla(160, 100%, 33%, 1));
}

button:active {
  transform: translateY(0);
}

button:disabled {
  background: #3a3a3a;
  color: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

h1 {
  color: hsla(160, 100%, 37%, 1);
  margin-bottom: 3rem;
  font-size: 2.5em;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.back-button {
  position: absolute;
  top: 2rem;
  left: 2rem;
  z-index: 10;
  padding: 0.8rem 1.5rem;
  text-transform: none;
  letter-spacing: 0.5px;
}

.error {
  color: #ff4444;
  text-align: center;
  margin: 2rem;
  padding: 1rem 2rem;
  background: rgba(255, 68, 68, 0.1);
  border-radius: 6px;
  border-left: 4px solid #ff4444;
}


</style>