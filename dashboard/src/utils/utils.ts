import { tick } from 'svelte';

export async function closeAndFocusTrigger(triggerId: string) {
  tick().then(() => {
    document.getElementById(triggerId)?.focus();
  });
}

export const availableModelProviders = ['Anthropic', 'Azure', 'Cohere', 'Google', 'Groq', 'Hugging Face', 'Mistral', 'OpenAI'];