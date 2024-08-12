<script lang="ts">
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
</script>

<thead>
  <tr>
    <th class="text-left p-2">
      <Skeleton class="h-6 w-24" />
    </th>
    <th class="text-left p-2">
      <Skeleton class="h-6 w-12" />
    </th>
    <th class="text-left p-2">
      <Skeleton class="h-6 w-24" />
    </th>
  </tr>
</thead>
<div class="mt-4 px-2 space-y-4">
  <Skeleton class="h-6 w-full" /> 
  <Skeleton class="h-6 w-full" />
  <Skeleton class="h-6 w-full" /> 
</div>