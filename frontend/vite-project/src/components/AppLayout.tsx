import {
    AppBar,
    Box,
    Drawer,
    IconButton,
    Toolbar,
    Typography,
    useMediaQuery,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useState } from "react";
import Sidebar from "./Sidebar";
import type { AppPage } from "./Sidebar";

interface Props {
    children: React.ReactNode;
    activePage: AppPage;
    onNavigate: (page: AppPage) => void;
}

const drawerWidth = 240;

export default function AppLayout({ children, activePage, onNavigate }: Props) {
    const isMobile = useMediaQuery("(max-width: 600px)");
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                <Toolbar>
                    {isMobile && (
                        <IconButton
                            color="inherit"
                            edge="start"
                            aria-label="Open navigation"
                            onClick={() => setMobileOpen(true)}
                            sx={{ mr: 2 }}
                        >
                            <MenuIcon />
                        </IconButton>
                    )}
                    <Typography variant="h6" component="h1" noWrap>
                        Enterprise Knowledge Intelligence Platform
                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                variant={isMobile ? "temporary" : "permanent"}
                open={!isMobile || mobileOpen}
                onClose={() => setMobileOpen(false)}
                sx={{
                    width: isMobile ? undefined : drawerWidth,
                    flexShrink: 0,
                    "& .MuiDrawer-paper": {
                        width: drawerWidth,
                        boxSizing: "border-box",
                    },
                }}
            >
                <Sidebar
                    activePage={activePage}
                    onNavigate={onNavigate}
                    onClose={() => setMobileOpen(false)}
                />
            </Drawer>
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    minWidth: 0,
                    p: { xs: 2, sm: 3 },
                    mt: 8,
                }}
            >
                {children}
            </Box>
        </Box>
    );
}