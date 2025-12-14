import * as React from "react";
import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {toast} from "react-toastify";
import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Stack,
    Typography,
    Button,
} from "@mui/material";
import {useAuthClient, useDeleteAuthClient} from "@app/features/auth/clients/hooks";


type FormDialogProps = {
    basePath: string;
};

export const FormDialog: React.FC<FormDialogProps> = ({basePath}) => {
    const navigate = useNavigate();
    const {action, recordId} = useParams();
    const [open, setOpen] = useState(false);
    const {data} = useAuthClient(recordId!);
    const deleteClient = useDeleteAuthClient();

    const closeDialog = () => {
        navigate(basePath);
    };

    const handleSubmit = async () => {
        try {
            await deleteClient.mutateAsync(recordId!);
            closeDialog();
            toast.success('API client deleted!');
        } catch (err: any) {
            if (err.response?.status < 200 || err.response?.status >= 300) {
                toast.error('API client could not be deleted!');
            } else {
                console.error(err);
                toast.error(err);
            }
        }
    };

    useEffect(() => {
        if (!action) {
            setOpen(false);
        } else if (action === 'delete') {
            setOpen(true);
        }
    }, [action]);

    return (
        <React.Fragment>
            <Dialog
                open={open}
                onClose={closeDialog}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">{data?.id ? 'Delete API Client?' : 'API Client Not Found!'}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        {data?.id ? (
                            <>
                                <Typography variant="body1" mb={4}>
                                    Are you absolutely sure you want to delete this API client?
                                </Typography>
                                <Stack spacing={1}>
                                    {data?.id && (<Typography variant="body1">API Client ID: {data?.id}</Typography>)}
                                    {data?.tenantId && (<Typography variant="body1">Tenant ID: {data?.tenantId}</Typography>)}
                                    {data?.userId && (<Typography variant="body1">User ID: {data?.userId}</Typography>)}
                                    {data?.name && (<Typography variant="body1">Name: {data?.name}</Typography>)}
                                    {data?.redirectUri && (<Typography variant="body1">Redirect URI: {data?.redirectUri}</Typography>)}
                                    {data?.scopes && (<Typography variant="body1">Scopes: {data?.scopes.join(', ')}</Typography>)}
                                    {data?.enabled && (<Typography variant="body1">Enabled: {data?.enabled ? 'Yes' : 'No'}</Typography>)}
                                    {data?.createdAt && (<Typography variant="body1">Created At: {data?.createdAt}</Typography>)}
                                    {data?.updatedAt && (<Typography variant="body1">Updated At: {data?.updatedAt}</Typography>)}
                                    {data?.expiresAt && (<Typography variant="body1">Expires At: {data?.expiresAt}</Typography>)}
                                </Stack>
                            </>
                        ) : (
                            <>
                                <Typography variant="body1" color="error">
                                    No API client could be found with the ID provided!
                                </Typography>
                            </>
                        )}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeDialog}>{data?.id ? 'Cancel' : 'Close'}</Button>
                    {data?.id && (
                        <Button color="error" variant="contained" onClick={handleSubmit} autoFocus>Delete API Client</Button>
                    )}
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
}

export default FormDialog;