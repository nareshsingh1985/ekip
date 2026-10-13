import {
    List,
    ListItem,
    ListItemButton,
    ListItemText,
    Toolbar,
} from "@mui/material";

export type AppPage = "dashboard" | "chat" | "documents";

interface Props {
    activePage: AppPage;
    onNavigate: (page: AppPage) => void;
    onClose?: () => void;
}

const pages: { id: AppPage; label: string }[] = [
    { id: "dashboard", label: "Dashboard" },
    { id: "chat", label: "Chat assistant" },
    { id: "documents", label: "Document Upload" },
];

export default function Sidebar({ activePage, onNavigate, onClose }: Props) {
    return (
        <>
            <Toolbar />
            <List aria-label="Main navigation">
                {pages.map((page) => (
                    <ListItem key={page.id} disablePadding>
                        <ListItemButton
                            selected={activePage === page.id}
                            aria-current={activePage === page.id ? "page" : undefined}
                            onClick={() => {
                                onNavigate(page.id);
                                onClose?.();
                            }}
                        >
                            <ListItemText primary={page.label} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </>
    );
}