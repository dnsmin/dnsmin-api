import * as React from "react";
import {
    Box, Container, Stack, Grid, Typography, Divider, Skeleton,
    List, ListItem, ListItemIcon, ListItemText
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const Page = () => {
    return (
        <>
            <Container sx={{pt: 10}}>
                <Stack spacing={6}>
                    <Box sx={{display: 'flex', justifyContent: 'center'}}>
                        <Typography variant="h1" className="pageHeader">
                            Meet DNSMin. <span style={{fontWeight: 'normal'}}>Built for Big DNS.</span>
                        </Typography>
                    </Box>
                    <Grid container spacing={2}>
                        <Grid size={{sm: 12, md: 6}}>
                            <Skeleton variant="rectangular" height={'100%'}/>
                        </Grid>
                        <Grid size={{sm: 12, md: 6}}>
                            <p>DNSMin is a powerful tool for managing the PowerDNS server suite.</p>
                            <p>There are a number of use cases where DNSMin is useful:</p>
                            <List>
                                <ListItem>
                                    <ListItemIcon>
                                        <AddIcon/>
                                    </ListItemIcon>
                                    <ListItemText primary="Operating a multi-tenant DNS service"/>
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon>
                                        <AddIcon/>
                                    </ListItemIcon>
                                    <ListItemText primary="Managing split-horizon DNS for your organization"/>
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon>
                                        <AddIcon/>
                                    </ListItemIcon>
                                    <ListItemText primary="Splitting zone control to multiple organizational units"/>
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon>
                                        <AddIcon/>
                                    </ListItemIcon>
                                    <ListItemText primary="Isolating PowerDNS APIs with advanced protection"/>
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon>
                                        <AddIcon/>
                                    </ListItemIcon>
                                    <ListItemText
                                        primary="Providing advanced API capabilities for streamlined automation"/>
                                </ListItem>
                            </List>
                        </Grid>
                    </Grid>
                    <Divider/>
                </Stack>
            </Container>
        </>
    );
};

export default Page;
