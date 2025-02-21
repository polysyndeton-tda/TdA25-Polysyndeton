import type { ColumnDef } from "@tanstack/table-core";
import { renderComponent } from "$lib/components/ui/data-table/index.js";
import DataTableColumnSortButton from "./data-table-sortable-button.svelte";
import { Checkbox } from "$lib/components/ui/checkbox/index.js";
// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
type User = {
    uuid: string;
    createdAt: string;
    username: string;
    email: string;
    elo: number;
    wins: number;
    draws: number;
    losses: number;
};

 
export const columns: ColumnDef<User>[] = [
    {
        accessorKey: "username",
        header: ({ column }) =>
            renderComponent(DataTableColumnSortButton, {
              headerName: "Uživatelské jméno",
              onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },
    {
        accessorKey: "email",
        header: ({ column }) =>
          renderComponent(DataTableColumnSortButton, {
            headerName: "Email",
            onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },
    {
        accessorKey: "elo",
        header: ({ column }) =>
            renderComponent(DataTableColumnSortButton, {
              headerName: "ELO",
              onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },
    {
        accessorKey: "wins",
        header: ({ column }) =>
            renderComponent(DataTableColumnSortButton, {
              headerName: "Výhry",
              onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },
    {
        accessorKey: "draws",
        header: ({ column }) =>
            renderComponent(DataTableColumnSortButton, {
              headerName: "Remízy",
              onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },
    {
        accessorKey: "losses",
        header: ({ column }) =>
            renderComponent(DataTableColumnSortButton, {
              headerName: "Prohry",
              onclick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        }),
    },


    //A new column for hosting the checkbox
    {
        id: "select",
        header: ({ table }) =>
          renderComponent(Checkbox, {
            checked: table.getIsAllPageRowsSelected(),
            class: "checkbox",
            indeterminate:
              table.getIsSomePageRowsSelected() &&
              !table.getIsAllPageRowsSelected(),
            onCheckedChange: (value) => table.toggleAllPageRowsSelected(!!value),
            "aria-label": "Select all",
          }),
        cell: ({ row }) =>
          renderComponent(Checkbox, {
            checked: row.getIsSelected(),
            class: "checkbox",
            onCheckedChange: (value) => row.toggleSelected(!!value),
            "aria-label": "Select row",
          }),
        enableSorting: false,
        enableHiding: false,
      },
];