<script lang="ts">
  import { writable } from 'svelte/store';
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { cn } from "$lib/utils.js";
  import Check from "lucide-svelte/icons/check";
  import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
  import { availableModelProviders, closeAndFocusTrigger } from "../utils/utils";
  import { Slider } from "$lib/components/ui/slider";

  let selectedProvider = '';
  const maxTokens = writable(100);
  const guardRails = writable<string[]>([""]);

  function save() {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');
    toast.success(`${selectedProvider}'s configuration has been saved.`, {
      description: `${formatted_date}`,
    })
  }

  function addGuardRail() {
    guardRails.update(gr => [...gr, ""]);
  }

  function updateGuardRail(event: Event, index: number) {
    const input = event.target as HTMLInputElement;
    guardRails.update(gr => {
      gr[index] = input.value;
      return gr;
    });
  }

  function removeGuardRail(index: number) {
    guardRails.update(gr => {
      gr.splice(index, 1);
      return gr;
    });
  }

  let open = false;
  let temperature = [50];
  $: selectedValue = availableModelProviders.find((f) => f === selectedProvider) ?? "Select a provider...";
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Configuration</h1>
  <div class="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-20 px-64">
      <h3 class="text-xl font-semibold mb-2">Select a Model Provider</h3>
        <Popover.Root bind:open let:ids>
          <Popover.Trigger asChild let:builder>
            <Button
              builders={[builder]}
              variant="outline"
              role="combobox"
              aria-expanded={open}
              class="w-[200px] justify-between"
            >
              {selectedValue}
              <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
          </Popover.Trigger>
          <Popover.Content class="w-[200px] p-0">
            <Command.Root>
              <Command.Input placeholder="Search provider..." />
              <Command.Empty>No provider found.</Command.Empty>
              <Command.Group>
                {#each availableModelProviders as provider}
                  <Command.Item
                    value={provider}
                    onSelect={(currentValue) => {
                      selectedProvider = currentValue;
                      closeAndFocusTrigger(ids.trigger);
                      open = false;
                    }}
                  >
                    <Check
                      class={cn(
                        "mr-2 h-4 w-4",
                        selectedProvider !== provider && "text-transparent"
                      )}
                    />
                    {provider}
                  </Command.Item>
                {/each}
              </Command.Group>
            </Command.Root>
          </Popover.Content>
        </Popover.Root>
      <h3 class="text-xl font-semibold my-4">Model Settings</h3>
      <div class="mb-4">
        <label for="temperature" class="block font-semibold mb-1">Temperature</label>
        <Slider bind:value={temperature} max={100} step={1} />
        <span>{temperature[0]}</span>
      </div>
      <div class="mb-4">
        <label for="maxTokens" class="block font-semibold mb-1">Max Tokens</label>
        <input id="maxTokens" type="number" min="1" max="1000" bind:value={$maxTokens} class="w-full border p-2 rounded bg-white" />
      </div>

        <h3 class="text-xl font-semibold mb-4">Guard Rails</h3>
        {#each $guardRails as guardRail, index}
          <div class="mb-4 flex items-center">
            <input
              type="text"
              class="w-full border p-2 rounded mb-2 bg-white"
              placeholder="Add guard rail"
              bind:value={$guardRails[index]}
              on:input={(e) => updateGuardRail(e, index)}
            />
            {#if index > 0}
              <button on:click={() => removeGuardRail(index)} class="ml-2 text-red-500 hover:text-red-700">Remove</button>
            {/if}
          </div>
        {/each}
        <button on:click={addGuardRail} class="px-4 py-2 text-white rounded-lg bg-red-800 hover:bg-red-700 transition mb-4">Add Guard Rail</button>
        <div>
          <button on:click={save} class="px-4 py-2 text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Save</button>
        </div>
      </div>
    </div>
  </div>
</div>
