<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { z } from "zod";

  const dispatch = createEventDispatcher();

  const UsernameSchema = z.string().min(1, "Username is required");
  const PasswordSchema = z.string().min(6, "Password must be at least 6 characters");

  const LoginSchema = z.object({
    username: z.string().min(1, "Username is required"),
    password: z.string().min(6, "Password must be at least 6 characters"),
  });

  const RegisterSchema = LoginSchema.extend({
    confirmPassword: z.string().min(1, "Confirm password is required")
  }).refine(data => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"]
  });

  type LoginForm = z.infer<typeof LoginSchema>;
  type RegisterForm = z.infer<typeof RegisterSchema>;

  let form: LoginForm & { confirmPassword?: string } = {
    username: "",
    password: "",
    confirmPassword: "",
  };
  let showRegister = false;

  type FormErrors = Partial<Record<keyof RegisterForm | 'form', string[] | string>>;
  let errors: FormErrors = {};

  async function login() {
    errors = {};
    const result = LoginSchema.safeParse(form);

    if (!result.success) {
      errors = result.error.formErrors.fieldErrors;
      return;
    }

    const { username, password } = result.data;
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
      localStorage.setItem("username", username);
      localStorage.setItem("userid", data.userid);
      dispatch("loginSuccess");
    } else {
      errors.form = "Login failed";
  }
  }

  async function register() {
    errors = {};
    const result = RegisterSchema.safeParse(form);

    if (!result.success) {
      errors = result.error.formErrors.fieldErrors;
      return;
    }

    const { username, password } = result.data;
    const response = await fetch(`http://127.0.0.1:8000/user/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      alert("Registration successful");
      showRegister = false;
    } else {
      errors.form = "Registration failed";
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

<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
    {#if showRegister}
      <h1 class="text-3xl font-bold mb-4 text-center">Register</h1>
      <div class="mb-4">
        <input type="text" placeholder="Username" bind:value={form.username} on:keydown={handleKeydown} class="border rounded-lg p-2 w-full" />
        {#if errors.username}<p class="text-red-500 text-sm mt-1">{errors.username}</p>{/if}
      </div>
      <div class="mb-4">
        <input type="password" placeholder="Password" bind:value={form.password} on:keydown={handleKeydown} class="border rounded-lg p-2 w-full" />
        {#if errors.password}<p class="text-red-500 text-sm mt-1">{errors.password}</p>{/if}
      </div>
      <div class="mb-4">
        <input type="password" placeholder="Confirm Password" bind:value={form.confirmPassword} on:keydown={handleKeydown} class="border rounded-lg p-2 w-full" />
        {#if errors.confirmPassword}<p class="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>{/if}
      </div>
      <button on:click={register} class="px-4 py-2 bg-green-500 text-white rounded-lg w-full hover:bg-green-600 transition">
        Register
      </button>
      <div class="text-center mt-4">
        <button type="button" class="cursor-pointer text-blue-500 underline" on:click={() => showRegister = false}>Already have an account? Login here</button>
      </div>
    {:else}
      <h1 class="text-3xl font-bold mb-4 text-center">Login</h1>
      <div class="mb-4">
        <input type="text" placeholder="Username" bind:value={form.username} on:keydown={handleKeydown} class="border rounded-lg p-2 w-full" />
        {#if errors.username}<p class="text-red-500 text-sm mt-1">{errors.username}</p>{/if}
      </div>
      <div class="mb-4">
        <input type="password" placeholder="Password" bind:value={form.password} on:keydown={handleKeydown} class="border rounded-lg p-2 w-full" />
        {#if errors.password}<p class="text-red-500 text-sm mt-1">{errors.password}</p>{/if}
      </div>
      <button on:click={login} class="px-4 py-2 bg-blue-500 text-white rounded-lg w-full hover:bg-blue-600 transition">
        Login
      </button>
      <div class="text-center mt-4">
        <button type="button" class="cursor-pointer text-blue-500 underline" on:click={() => showRegister = true}>Don't have an account? Register here</button>
      </div>
    {/if}
    {#if errors.form}<p class="text-red-500 text-sm mt-4 text-center">{errors.form}</p>{/if}
  </div>
</div>