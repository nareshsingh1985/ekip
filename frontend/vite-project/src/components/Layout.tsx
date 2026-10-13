import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  AppBar,
  Typography,
  Box,
} from "@mui/material";

import { Link } from "react-router-dom";
import type { ReactNode } from "react";

const drawerWidth = 240;

export default function Layout({
  children,
}: { children: ReactNode }) {

  return (
    <Box sx={{ display: "flex" }}>

      <AppBar
        position="fixed"
      >
        <Toolbar>
          <Typography
            variant="h6"
          >
            EKIP
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
        }}
      >

        <Toolbar />

        <List>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/"
            >
              <ListItemText
                primary="Dashboard"
              />
            </ListItemButton>
          </ListItem>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/search"
            >
              <ListItemText
                primary="Search"
              />
            </ListItemButton>
          </ListItem>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/documents"
            >
              <ListItemText
                primary="Documents"
              />
            </ListItemButton>
          </ListItem>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/insights"
            >
              <ListItemText
                primary="Insights"
              />
            </ListItemButton>
          </ListItem>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/graph"
            >
              <ListItemText
                primary="Knowledge Graph"
              />
            </ListItemButton>
          </ListItem>

          <ListItem disablePadding>
            <ListItemButton
              component={Link}
              to="/assistant"
            >
              <ListItemText
                primary="AI Assistant"
              />
            </ListItemButton>
          </ListItem>

        </List>

      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
        }}
      >
        <Toolbar />

        {children}

      </Box>

    </Box>
  );
}