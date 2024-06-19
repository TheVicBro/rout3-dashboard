<script lang="ts">
  import { createEventDispatcher } from "svelte";
  let username = "";
  let password = "";
  const dispatch = createEventDispatcher();

  async function login() {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const credentials = btoa(`${username}:${password}`);

    const response = await fetch(`http://127.0.0.1:8000/user/login`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${credentials}`,
      },
    });

    if (response.ok) {
      const { token } = await response.json();
      localStorage.setItem("authToken", token);
      dispatch("loginSuccess");
    } else {
      alert("Login failed");
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
    <h1 class="text-3xl font-bold mb-4 text-center">Login</h1>
    <input
      type="text"
      placeholder="Username"
      bind:value={username}
      class="border rounded-lg p-2 mb-4 w-full"
    />
    <input
      type="password"
      placeholder="Password"
      bind:value={password}
      class="border rounded-lg p-2 mb-4 w-full"
    />
    <button
      on:click={login}
      class="px-4 py-2 bg-blue-500 text-white rounded-lg w-full hover:bg-blue-600 transition"
      >Login</button
    >
  </div>
</div>
