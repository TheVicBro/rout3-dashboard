<script lang="ts">
  import { DateTime } from 'luxon';
  import { Label } from "$lib/components/ui/label/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Card } from "$lib/components/ui/card/index.js";
  import { writable } from "svelte/store";
  import { Loader2 } from 'lucide-svelte';

  interface ChatMessage {
    role: "user" | "bot";
    content: string;
  }

  interface ApiResponse {
    model: string;
    prompt: string;
    response: string;
    chat_history: ChatMessage[];
    prompt_cost: number;
    response_cost: number;
    prompt_tokens: number;
    response_tokens: number;
    date_time: string;
    user_id: number;
  }

  interface DisplayMessage {
    sender: "user" | "assistant";
    text: string;
    model?: string;
  }

  let message = '';
  let myAPI = '';
  let chatHistory: ChatMessage[] = [];
  let isLoading = false;
  const messages = writable<DisplayMessage[]>([]);

  const sendMessage = async () => {
    if (message.trim() === "") return;
    isLoading = true;

    // Add user message to chat history
    chatHistory.push({ role: "user", content: message });
    messages.update((msgs) => [...msgs, { sender: "user", text: message }]);
    message = "";

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/router/completion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "myapi-key": myAPI,
        },
        body: JSON.stringify({
          chat_history: chatHistory
        }),
      });

      const responseText = await response.text();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${responseText}`);
      }

      const responseData: ApiResponse = JSON.parse(responseText);

      if (responseData.response) {
        // Add bot response to chat history
        chatHistory = responseData.chat_history;
        messages.update((msgs) => [...msgs, { 
          sender: "assistant", 
          text: responseData.response,
          model: responseData.model
        }]);
      } else {
        throw new Error("Unexpected response format");
      }
    } catch (error) {
      console.error("Error fetching response:", error);
      let errorMessage = "Something went wrong. Please try again.";
      if (error instanceof Error) {
        errorMessage += ` Error details: ${error.message}`;
      }
      messages.update((msgs) => [...msgs, { sender: "assistant", text: errorMessage, model: "Error" }]);
      toast.error(errorMessage);
    }
    isLoading = false;
  };
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white dark:bg-slate-900 border-b-2 dark:border-black">Chat</h1>
  <div class="flex-1 overflow-auto">
    <div class="h-full m-10 border dark:border-black rounded-lg bg-white dark:bg-slate-900 shadow">
      <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2 dark:border-black">Overview</h2>
      <div class="h-full p-10 px-20 space-y-8">
        <h3 class="text-2xl text-bold">Test your Rout3 here</h3>
        <Input type="text" bind:value={myAPI} placeholder="Enter your MyAPI key here..." />
        <div class="mt-64">
          <Card class="p-4 space-y-4">
            <div class="overflow-y-auto max-h-[400px]">
              {#each $messages as msg (msg.text)}
                <div class="mb-2">
                  <strong>{msg.sender === "user" ? "You" : msg.model}:</strong> {msg.text}
                </div>
              {/each}
              {#if isLoading}
                <div class="flex items-center space-x-2">
                  <Loader2 class="animate-spin" />
                  <span>Thinking...</span>
                </div>
              {/if}
            </div>

            <div class="flex space-x-2">
              <Input
                type="text"
                bind:value={message}
                placeholder="Type your message..."
                class="flex-1"
                on:keydown={(e) => e.key === "Enter" && sendMessage()}
              />
              <Button on:click={sendMessage} class="text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Send</Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</div>
