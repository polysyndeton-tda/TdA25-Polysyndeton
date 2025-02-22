<script lang="ts" generics="TData, TValue">
import { type ColumnDef, getCoreRowModel, type PaginationState, type SortingState, type ColumnFiltersState, type RowSelectionState, getPaginationRowModel, getSortedRowModel, getFilteredRowModel } from "@tanstack/table-core";
import { 
    createSvelteTable,
    FlexRender,
} from "$lib/components/ui/data-table/index.js";
import * as Table from "$lib/components/ui/table/index.js";
import { Button } from "$lib/components/ui/button/index.js";
import Input from "$lib/components/ui/input/input.svelte";
import * as Select from "$lib/components/ui/select/index.js";
 
type DataTableProps<TData, TValue> = {
    columns: ColumnDef<TData, TValue>[];
    data: TData[];
    tableReference: any;
    selectedRows: any
    classesToSet: string
};
 
let { data, columns, tableReference = $bindable(), selectedRows = $bindable(), classesToSet }: DataTableProps<TData, TValue> = $props();

let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });
let sorting = $state<SortingState>([]);
let columnFilters = $state<ColumnFiltersState>([]);
let rowSelection = $state<RowSelectionState>({});
// $inspect(rowSelection);

// would be great if selectedRows = $derived(rowSelection); worked
//otherwise using this:
$effect(() => {
    selectedRows = rowSelection;
})
 
const table = createSvelteTable({
    get data() {
        return data;
    },
    columns,
    state: {
        get pagination() {
            return pagination;
        },
        get sorting() {
            return sorting;
        },
        get columnFilters() {
            return columnFilters;
        },
        get rowSelection() {
            return rowSelection;
        },
    },
    onSortingChange: (updater) => {
      if (typeof updater === "function") {
        sorting = updater(sorting);
      } else {
        sorting = updater;
      }
    },
    onPaginationChange: (updater) => {
        if (typeof updater === "function") {
            pagination = updater(pagination);
        } else {
            pagination = updater;
        }
    },
    onColumnFiltersChange: (updater) => {
      if (typeof updater === "function") {
        columnFilters = updater(columnFilters);
      } else {
        columnFilters = updater;
      }
    },
    onRowSelectionChange: (updater) => {
      if (typeof updater === "function") {
        rowSelection = updater(rowSelection);
      } else {
        rowSelection = updater;
      }
    },
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
});

tableReference = table;

function selectThisRowAndUnselectOthers(event: any, table: any, row: any){
    //On right click, we want to select the row if no rows are selected, 
    // but otherwise if there is a selection, we don't want to cancel it
    if(event.type == "contextmenu"){
        row.toggleSelected(true);
        return;
    }

    if (!event.target.closest('.checkbox')) {
        if(!(event.ctrlKey || event.shiftKey)){
             //unselect all rows
            table.toggleAllPageRowsSelected(false);
            //select this row in particular
            row.toggleSelected(true);
        }else{
            //if shift or ctrl is held down, it makes sense to select more rows, the same as checkbox
            row.toggleSelected(!row.getIsSelected());
        }
        
    }
    console.log("Row select ran");
   
}


const valuesToEN = {
  "Emailu": "email",
  "Uživatelského jména": "username",
  "ELO": "elo",
  "Výher": "wins",
  "Remíz": "draws",
  "Proher": "losses"
};

const valuesToCZ = {
  "email": "Emailu",
  "username": "Uživatelského jména",
  "elo": "ELO",
  "wins": "Výher",
  "draws": "Remíz",
  "losses": "Proher"
};

let filterValue: any = $state("email");
let searchQuery: string = $state("");

</script>

<div>
    <div class="flex items-center py-4 {classesToSet} gap-[4px]">
        <Input
        placeholder="Filtrovat podle..."
        value={(table.getColumn($state.snapshot(filterValue)).getFilterValue() as string) ?? ""}
        onchange={(e) => {
            searchQuery = e.currentTarget.value;
            table.getColumn($state.snapshot(filterValue)).setFilterValue(searchQuery);
        }}
        oninput={(e) => {
            searchQuery = e.currentTarget.value;
            table.getColumn($state.snapshot(filterValue)).setFilterValue(searchQuery);
        }}
        class="max-w-sm"
        />

        <Select.Root type="single" bind:value={filterValue}> 
            <Select.Trigger class="w-[180px]">{valuesToCZ[filterValue]}</Select.Trigger>
            <Select.Content>
              <Select.Item value="email">Emailu</Select.Item>
              <Select.Item value="username">Uživatelského jména</Select.Item>
              <!-- <Select.Item value="elo">ELO</Select.Item>
              <Select.Item value="wins">Výher</Select.Item>
              <Select.Item value="draws">Remíz</Select.Item>
              <Select.Item value="losses">Proher</Select.Item> -->
            </Select.Content>
          </Select.Root>
    </div>
    <div class="rounded-md border {classesToSet}">
    <Table.Root>
        <Table.Header>
        {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
            <Table.Row>
            {#each headerGroup.headers as header (header.id)}
                <Table.Head>
                {#if !header.isPlaceholder}
                    <FlexRender
                    content={header.column.columnDef.header}
                    context={header.getContext()}
                    />
                {/if}
                </Table.Head>
            {/each}
            </Table.Row>
        {/each}
        </Table.Header>
        <Table.Body>
        {#each table.getRowModel().rows as row (row.id)}
            <Table.Row data-state={row.getIsSelected() && "selected"} onclick={(event) => selectThisRowAndUnselectOthers(event, table, row)} oncontextmenu={(event) => selectThisRowAndUnselectOthers(event, table, row)}>
            {#each row.getVisibleCells() as cell (cell.id)}
                <Table.Cell>
                <FlexRender
                    content={cell.column.columnDef.cell}
                    context={cell.getContext()}
                />
                </Table.Cell>
            {/each}
            </Table.Row>
        {:else}
            <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
                No results.
            </Table.Cell>
            </Table.Row>
        {/each}
        </Table.Body>
    </Table.Root>
    </div>
    

    <div class="text-muted-foreground flex-1 text-sm pl-[8px]">
        {table.getFilteredSelectedRowModel().rows.length} z{" "}
        {table.getState().pagination.pageSize} řádků na stránce vybráno. | <!-- this showed up all users number (11 not 10) table.getFilteredRowModel().rows.length -->
        Celkově {table.getRowCount()} uživatelů.
    </div>
  
  

    <div class="flex items-center justify-end space-x-2 py-4">
                    <!-- 0 indexed so + 1 -->
        <p>Stránka {table.getState().pagination.pageIndex + 1} z {table.getPageCount()}</p>
        <Button
        variant="outline"
        size="sm"
        onclick={() => table.previousPage()}
        disabled={!table.getCanPreviousPage()}
        >
        Previous
        </Button>
        <Button
        variant="outline"
        size="sm"
        onclick={() => table.nextPage()}
        disabled={!table.getCanNextPage()}
        >
        Next
        </Button>
    </div>
</div>