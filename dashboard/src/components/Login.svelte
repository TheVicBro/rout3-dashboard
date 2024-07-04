<script lang="ts">
  import { createEventDispatcher } from "svelte";

  let username = "";
  let password = "";
  let confirmPassword = "";
  const dispatch = createEventDispatcher();
  let showRegister = false;

  async function login() {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`http://127.0.0.1:8000/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("authToken", data.access_token);
      dispatch("loginSuccess");
    } else {
      alert("Login failed");
    }
  }

  async function register() {
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const response = await fetch(`http://127.0.0.1:8000/user/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    if (response.ok) {
      alert("Registration successful");
      showRegister = false;
    } else {
      alert("Registration failed");
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      if (showRegister) {
        register();
      } else {
        login();
      }
    }
  }
</script>

<style>
  .toggle-button {
    cursor: pointer;
    color: blue;
    text-decoration: underline;
  }
</style>

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
    {#if showRegister}
      <h1 class="text-3xl font-bold mb-4 text-center">Register</h1>
      <input
        type="text"
        placeholder="Username"
        bind:value={username}
        on:keydown={handleKeydown}
        class="border rounded-lg p-2 mb-4 w-full"
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={password}
        on:keydown={handleKeydown}
        class="border rounded-lg p-2 mb-4 w-full"
      />
      <input
        type="password"
        placeholder="Confirm Password"
        bind:value={confirmPassword}
        on:keydown={handleKeydown}
        class="border rounded-lg p-2 mb-4 w-full"
      />
      <button
        on:click={register}
        class="px-4 py-2 bg-green-500 text-white rounded-lg w-full hover:bg-green-600 transition"
        >Register</button
      >

      <div class="text-center mt-4">
        <span class="toggle-button" on:click={() => showRegister = false}>Already have an account? Login here</span>
      </div>
    {:else}
      <h1 class="text-3xl font-bold mb-4 text-center">Login</h1>
      <input
        type="text"
        placeholder="Username"
        bind:value={username}
        on:keydown={handleKeydown}
        class="border rounded-lg p-2 mb-4 w-full"
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={password}
        on:keydown={handleKeydown}
        class="border rounded-lg p-2 mb-4 w-full"
      />
      <button
        on:click={login}
        class="px-4 py-2 bg-blue-500 text-white rounded-lg w-full hover:bg-blue-600 transition"
        >Login</button
      >

      <div class="text-center mt-4">
        <span class="toggle-button" on:click={() => showRegister = true}>Don't have an account? Register here</span>
      </div>
    {/if}
  </div>
</div>
