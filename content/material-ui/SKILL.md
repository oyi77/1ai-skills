---
name: material-ui
description: Material UI (MUI) React components — theming, styled engine, data grid, date pickers, icons
---

## Overview

Material UI (MUI) is a comprehensive React component library implementing Google's Material Design. Includes components, icons, date pickers, data grid, and a powerful theming system with styled-engine.

## Capabilities

- 100+ production-ready Material Design components
- Theming with createTheme (colors, typography, spacing, breakpoints)
- sx prop for inline styling with theme access
- MUI X: DataGrid, DatePicker, TreeView, Charts
- 2000+ Material Design icons
- CSS-in-JS with Emotion or styled-components

## When to Use

- Building enterprise React applications with Material Design
- Need advanced data tables with sorting, filtering, pagination
- Want a mature, well-documented component ecosystem
- Building admin panels, dashboards, data-heavy apps

## Pseudo Code

### Installation
```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
# Optional: DataGrid, DatePicker
npm install @mui/x-data-grid @mui/x-date-pickers
```

### Theme Setup
```tsx
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material"

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#9c27b0" },
    mode: "light",
  },
  typography: { fontFamily: "Inter, Roboto, sans-serif" },
  shape: { borderRadius: 8 },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <YourApp />
    </ThemeProvider>
  )
}
```

### sx Prop Styling
```tsx
import { Box, Typography, Button } from "@mui/material"

export function Dashboard() {
  return (
    <Box sx={{ p: 4, display: "flex", gap: 2, bgcolor: "background.paper" }}>
      <Typography variant="h4" sx={{ fontWeight: 600 }}>
        Dashboard
      </Typography>
      <Button variant="contained" sx={{ ml: "auto" }}>
        Export
      </Button>
    </Box>
  )
}
```

### DataGrid
```tsx
import { DataGrid } from "@mui/x-data-grid"

const columns = [
  { field: "id", headerName: "ID", width: 90 },
  { field: "name", headerName: "Name", flex: 1 },
  { field: "status", headerName: "Status", width: 120 },
]

export function DataTable({ rows }) {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      pageSize={25}
      checkboxSelection
      disableRowSelectionOnClick
    />
  )
}
```

## Common Patterns

- **Theme tokens**: `sx={{ color: "primary.main", bgcolor: "grey.100" }}`
- **Responsive**: `sx={{ display: { xs: "none", md: "flex" } }}`
- **Styled API**: `const StyledBox = styled(Box)(({ theme }) => ({ padding: theme.spacing(2) }))`
- **Breakpoints**: `theme.breakpoints.up("sm")` for responsive queries
- **Component override**: `components: { MuiButton: { styleOverrides: { root: { textTransform: "none" } } } }`
