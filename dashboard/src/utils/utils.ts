import { tick } from 'svelte';

export async function closeAndFocusTrigger(triggerId: string) {
  tick().then(() => {
    document.getElementById(triggerId)?.focus();
  });
}

export const availableModelProviders = ['OpenAI', 'Hugging Face', 'Google', 'Azure', 'Cohere', 'Mistral'];