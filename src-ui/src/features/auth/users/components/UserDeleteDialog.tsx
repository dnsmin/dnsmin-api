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
import {useUser, useDeleteUser} from "@app/features/auth/users/hooks";


type FormDialogProps = {
    basePath: string;
};

export const FormDialog: React.FC<FormDialogProps> = ({basePath}) => {
    const navigate = useNavigate();
    const {action, recordId} = useParams();
    const [open, setOpen] = useState(false);
    const {data} = useUser(recordId!);
    const deleteUser = useDeleteUser();

    const closeDialog = () => {
        navigate(basePath);
    };

    const handleSubmit = async () => {
        try {
            await deleteUser.mutateAsync(recordId!);
            closeDialog();
            toast.success('User deleted!');
        } catch (err: any) {
            if (err.response?.status < 200 || err.response?.status >= 300) {
                toast.error('User could not be deleted!');
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
                <DialogTitle id="alert-dialog-title">{data?.id ? 'Delete User?' : 'User Not Found!'}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        {data?.id ? (
                            <>
                                <Typography variant="body1" mb={4}>
                                    Are you absolutely sure you want to delete this user and all their owned data?
                                </Typography>
                                <Stack spacing={1}>
                                    {data?.id && (<Typography variant="body1">User ID: {data?.id}</Typography>)}
                                    {data?.username && (<Typography variant="body1">Username: {data?.username}</Typography>)}
                                    {data?.email && (<Typography variant="body1">Email: {data?.email}</Typography>)}
                                    {data?.phoneNumber && (<Typography variant="body1">Phone Number: {data?.phoneNumber}</Typography>)}
                                    {data?.createdAt && (<Typography variant="body1">Created At: {data?.createdAt}</Typography>)}
                                    {data?.updatedAt && (<Typography variant="body1">Updated At: {data?.updatedAt}</Typography>)}
                                    {data?.authenticatedAt && (<Typography variant="body1">Last Authenticated At: {data?.authenticatedAt}</Typography>)}
                                </Stack>
                            </>
                        ) : (
                            <>
                                <Typography variant="body1" color="error">
                                    No user could be found with the ID provided!
                                </Typography>
                            </>
                        )}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeDialog}>{data?.id ? 'Cancel' : 'Close'}</Button>
                    {data?.id && (
                        <Button color="error" variant="contained" onClick={handleSubmit} autoFocus>Delete User</Button>
                    )}
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
}

export default FormDialog;