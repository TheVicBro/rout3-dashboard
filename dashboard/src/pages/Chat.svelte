<script lang="ts">
  import { DateTime } from 'luxon';
  import { Label } from "$lib/components/ui/label/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Card } from "$lib/components/ui/card/index.js";
  import { get, writable } from "svelte/store";
  import { Loader2 } from 'lucide-svelte';
  import { onMount } from 'svelte';

  interface ChatMessage {
    role: "user" | "assistant";
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
  let chatHistory: ChatMessage[] = [];
  let isLoading = false;
  let clearText = "Clear Chat";
  const myAPI = writable('');
  const messages = writable<DisplayMessage[]>([]);

  onMount(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    if (savedMessages) {
      messages.set(JSON.parse(savedMessages));
    }
    
    const savedChatHistory = localStorage.getItem('chatHistory');
    if (savedChatHistory) {
      const parsedHistory = JSON.parse(savedChatHistory);
      chatHistory = parsedHistory.map((msg: any) => ({
        ...msg,
        role: msg.role === 'bot' ? 'assistant' : msg.role
      }));
    }

    const savedAPIKey = localStorage.getItem('myAPIKey');
    if (savedAPIKey) {
      myAPI.set(savedAPIKey);
    }

    // Subscribe to changes in messages store and save to localStorage
    messages.subscribe(value => {
      localStorage.setItem('chatMessages', JSON.stringify(value));
    });

    myAPI.subscribe(value => {
      localStorage.setItem('myAPIKey', value);
    });
  });

  const sendMessage = async () => {
    if (message.trim() === "") return;
    isLoading = true;

    // Add user message to chat history
    chatHistory.push({ role: "user", content: message });
    messages.update((msgs) => [...msgs, { sender: "user", text: message }]);
    const currentAPIKey = get(myAPI); // Get current API key
    message = "";

    // Save updated chat history to localStorage
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

    try {
      const response = await fetch("https://rout3-backend.vercel.app/api/v1/router/completion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "myapi-key": currentAPIKey,
        },
        body: JSON.stringify({
          chat_history: chatHistory
        }),
      });

      const responseText = await response.text();

      if (!response.ok) {
        chatHistory.pop();
        messages.update((msgs) => msgs.slice(0, -1));
        if (response.status === 401) {
          throw new Error("Could not validate MyAPI or Secret key");
        } else
        if (response.status === 404) {
          throw new Error("No model configurations added.");
        }
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
      let errorMessage = error instanceof Error ? error.message : "An error occurred";
      toast.error(errorMessage);
    } finally {
      isLoading = false;
    }
  };

  const clearChat = () => {
    chatHistory = [];
    messages.set([]);
    localStorage.removeItem('chatHistory');
    localStorage.removeItem('chatMessages');
    clearText = 'Cleared!';
    setTimeout(() => {
      clearText = 'Clear Chat';
    }, 2000);
  };
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 text-3xl font-bold bg-white dark:bg-slate-900 border-b dark:border-slate-800">Chat</h1>
    <div class="m-10 flex-1 flex flex-col bg-white dark:bg-slate-900 rounded-lg border dark:border-slate-800 shadow-sm overflow-hidden">
      <div class="p-6 border-b dark:border-slate-800 flex justify-between items-center">
        <h2 class="text-2xl font-semibold">Playground</h2>
        <div class="flex items-center gap-4">
           <Input type="password" bind:value={$myAPI} placeholder="Enter MyAPI Key..." class="w-64" />
           <Button variant="outline" on:click={clearChat} size="sm">{clearText}</Button>
        </div>
      </div>
      
      <div class="flex-1 flex flex-col p-6 overflow-hidden">
          <div class="flex-1 overflow-y-auto space-y-4 p-4 rounded-lg border dark:border-slate-800 bg-gray-50 dark:bg-slate-950/50 mb-4">
            {#if $messages.length === 0}
              <div class="h-full flex flex-col items-center justify-center text-gray-400">
                <p>Start a conversation to test your routing.</p>
              </div>
            {/if}
            {#each $messages as msg (msg.text)}
              <div class={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div class={`max-w-[80%] rounded-2xl px-4 py-2 ${
                  msg.sender === "user" 
                    ? "bg-blue-600 text-white rounded-br-none" 
                    : "bg-white dark:bg-slate-800 border dark:border-slate-700 rounded-bl-none"
                }`}>
                  {#if msg.sender === "assistant" && msg.model}
                    <div class="text-xs text-gray-500 dark:text-gray-400 mb-1 font-mono">{msg.model}</div>
                  {/if}
                  <p class="whitespace-pre-wrap">{msg.text}</p>
                </div>
              </div>
            {/each}
            {#if isLoading}
              <div class="flex justify-start">
                <div class="bg-white dark:bg-slate-800 border dark:border-slate-700 rounded-2xl rounded-bl-none px-4 py-2 flex items-center space-x-2">
                  <Loader2 class="h-4 w-4 animate-spin" />
                  <span class="text-sm text-gray-500">Thinking...</span>
                </div>
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
            <Button on:click={sendMessage} class="bg-blue-600 hover:bg-blue-700 text-white px-8">Send</Button>
          </div>
      </div>
    </div>
</div>
