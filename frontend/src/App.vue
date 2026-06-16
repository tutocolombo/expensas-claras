<script setup lang="ts">
import { ref } from "vue"

const message = ref("")
const reply = ref("")
const loading = ref(false)

async function send() {
  if (!message.value.trim()) return
  loading.value = true
  try {
    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "default",
        feature: "example",
        message: message.value,
      }),
    })
    const data = await res.json()
    reply.value = data.message
  } catch {
    reply.value = "Error connecting to backend."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main>
    <h1>Expensas Claras</h1>
    <textarea v-model="message" placeholder="Type your message..." rows="4" />
    <button :disabled="loading" @click="send">
      {{ loading ? "Sending..." : "Send" }}
    </button>
    <p v-if="reply">{{ reply }}</p>
  </main>
</template>
