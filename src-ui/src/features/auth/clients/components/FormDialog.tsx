import * as React from "react";
import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {toast} from "react-toastify";
import {Formik, FormikHelpers} from "formik";
import {object, string} from "yup";
import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Typography,
    Grid,
    Stack,
    Button,
    TextField,
    FormControl,
    FormHelperText,
    InputLabel,
    Select,
    MenuItem,

} from "@mui/material";
import {useAuthClient, useCreateAuthClient, useUpdateAuthClient} from "@app/features/auth/clients/hooks";
import {mapFastApiErrorsToFormik} from "@app/utils/fastapi-formik";
import {IClient} from "@app/features/auth/clients/models";

type FormDialogProps = {
    basePath: string;
};

interface formRequirements {
    nameRequired: boolean;
    nameMinLength: number;
    nameMaxLength: number;
    secretRequired: boolean;
    secretMinLength: number;
    secretMaxLength: number;
    redirectUriRequired: boolean;
    redirectUriMinLength: number;
    redirectUriMaxLength: number;
    enabledRequired: boolean;
    tenantIdRequired: boolean;
    tenantIdLength: number;
    userIdRequired: boolean;
    userIdLength: number;
}

const formReqs: formRequirements = {
    nameRequired: true,
    nameMinLength: 4,
    nameMaxLength: 100,
    secretRequired: true,
    secretMinLength: 4,
    secretMaxLength: 100,
    redirectUriRequired: true,
    redirectUriMinLength: 3,
    redirectUriMaxLength: 100,
    enabledRequired: true,
    tenantIdRequired: false,
    tenantIdLength: 32,
    userIdRequired: false,
    userIdLength: 32,
};

const getValidationSchema = (isEdit: boolean) => {
    const schema = {
        name: string()
            .required('Client name is required.')
            .min(formReqs.nameMinLength, `Client name must be at least ${formReqs.nameMinLength} characters.`)
            .max(formReqs.nameMaxLength, `Client name must be at most ${formReqs.nameMaxLength} characters.`),
        secret: string().nullable()
            .min(formReqs.secretMinLength, `Secret must be at least ${formReqs.secretMinLength} characters.`)
            .max(formReqs.secretMaxLength, `Secret must be at most ${formReqs.secretMaxLength} characters.`),
        redirectUri: string()
            //.required('Redirect URI is required.')
            .min(formReqs.redirectUriMinLength, `Redirect URI must be at least ${formReqs.redirectUriMinLength} characters.`)
            .max(formReqs.redirectUriMaxLength, `Redirect URI must be at most ${formReqs.redirectUriMaxLength} characters.`),
        enabled: string()
            .required('Status is required.'),
        tenantId: string()
            .length(formReqs.tenantIdLength, 'Tenant ID is not valid.'),
        userId: string()
            .length(formReqs.userIdLength, 'User ID is not valid.'),
    };

    if (!isEdit) {
        schema.secret = schema.secret.required('Secret is required.');
    }

    return object(schema);
};

export const FormDialog: React.FC<FormDialogProps> = ({basePath}) => {
    const navigate = useNavigate();
    const {action, recordId} = useParams();
    const isEdit = !!recordId;
    const [open, setOpen] = useState(false);
    const {data} = useAuthClient(recordId!);
    const createClient = useCreateAuthClient();
    const updateClient = useUpdateAuthClient(recordId!);
    const isValid = !recordId || (recordId && data?.id);

    const initialValues: IClient = isEdit
        ? {
            tenantId: data?.tenantId ?? '',
            userId: data?.userId ?? '',
            name: data?.name ?? '',
            secret: '',
            redirectUri: data?.redirectUri ?? '',
            scopes: data?.scopes ?? [],
            enabled: data?.enabled ?? false,
        }
        : {
            tenantId: '',
            userId: '',
            name: '',
            secret: '',
            redirectUri: '',
            scopes: [],
            enabled: false,
        };

    const closeDialog = () => {
        navigate(basePath);
    };

    const handleSubmit = async (values: IClient, actions: FormikHelpers<IClient>) => {
        try {
            if (isEdit) {
                await updateClient.mutateAsync(values);
            } else {
                await createClient.mutateAsync(values);
            }
            closeDialog();
            actions.resetForm();
            actions.setStatus();
            toast.success('API client saved!');
        } catch (err: any) {
            if (err.response?.status === 422 && err.response.data?.detail) {
                actions.setErrors(mapFastApiErrorsToFormik(err.response.data.detail));
                toast.error('API client could not be saved!');
            } else {
                console.error(err);
                toast.error(err);
            }
            actions.setStatus('API client could not be saved!');
        }
        actions.setSubmitting(false);
    };

    useEffect(() => {
        if (!action) {
            setOpen(false);
        } else if (action === 'create') {
            setOpen(true);
        } else if (action === 'update') {
            setOpen(true);
        }
    }, [action]);

    return (
        <React.Fragment>
            <Dialog
                fullWidth={true}
                maxWidth={isValid ? 'md' : 'sm'}
                open={open}
                onClose={closeDialog}
            >
                <Formik
                    initialValues={initialValues}
                    validationSchema={getValidationSchema(isEdit)}
                    enableReinitialize={true}
                    validateOnChange={false}
                    validateOnBlur={false}
                    onSubmit={handleSubmit}
                >
                    {form => (
                        <form onSubmit={form.handleSubmit} onReset={form.handleReset}>
                            <DialogTitle>
                                {recordId && !data?.id ? 'API Client Not Found!' : (
                                    <>{isEdit ? 'Update' : 'Create'} API Client</>
                                )}
                            </DialogTitle>
                            <DialogContent>
                                <DialogContentText>
                                    {!isValid ? (
                                        <>
                                            <Typography variant="body1" color="error">
                                                No API client could be found with the ID provided!
                                            </Typography>
                                        </>
                                    ) : (
                                        <>
                                            {isEdit ? (
                                                <Typography variant="body1">
                                                    Please make the desired changes and then click Update API Client
                                                    when finished.
                                                </Typography>
                                            ) : (
                                                <Typography variant="body1">
                                                    Please provide the following details and then click Create API
                                                    Client when finished.
                                                </Typography>
                                            )}
                                            {form.status && (
                                                <>
                                                    <Typography variant="body1" color="error"
                                                                className="formStatus">{form.status}</Typography>
                                                </>
                                            )}
                                        </>
                                    )}
                                </DialogContentText>
                                {isValid && (
                                    <>
                                        <Grid container marginY={2}>
                                            <Grid size={{xs: 12, md: 6}}>
                                                <Typography variant="h6" align="center" gutterBottom>API Client
                                                    Information</Typography>
                                                <Stack component="form" spacing={3} noValidate>
                                                    <TextField
                                                        label="Name"
                                                        variant="outlined"
                                                        fullWidth
                                                        {...form.getFieldProps('name')}
                                                        error={form.errors.name !== undefined}
                                                        helperText={form.errors.name?.toString()}
                                                    />

                                                    <TextField
                                                        label="Secret"
                                                        type="password"
                                                        variant="outlined"
                                                        fullWidth
                                                        {...form.getFieldProps('secret')}
                                                        error={form.errors.secret !== undefined}
                                                        helperText={form.errors.secret?.toString()}
                                                    />

                                                    <TextField
                                                        label="Redirect URI"
                                                        type="text"
                                                        variant="outlined"
                                                        fullWidth
                                                        {...form.getFieldProps('redirectUri')}
                                                        error={form.errors.redirectUri !== undefined}
                                                        helperText={form.errors.redirectUri?.toString()}
                                                    />

                                                    <FormControl fullWidth variant="outlined">
                                                        <InputLabel id="enabled-label">Status</InputLabel>
                                                        <Select
                                                            labelId="enabled-label"
                                                            id="enabled"
                                                            label="Status"
                                                            {...form.getFieldProps('enabled')}
                                                            error={form.errors.enabled !== undefined}
                                                        >
                                                            <MenuItem value={'false'}>Disabled</MenuItem>
                                                            <MenuItem value={'true'}>Enabled</MenuItem>
                                                        </Select>
                                                        <FormHelperText>{form.errors.enabled?.toString()}</FormHelperText>
                                                    </FormControl>

                                                    <FormControl fullWidth variant="outlined">
                                                        <InputLabel id="tenant-label">Tenant</InputLabel>
                                                        <Select
                                                            labelId="tenant-label"
                                                            id="tenant"
                                                            label="Tenant"
                                                            {...form.getFieldProps('tenantId')}
                                                            error={form.errors.tenantId !== undefined}
                                                        >
                                                            <MenuItem value="">
                                                                <em>None</em>
                                                            </MenuItem>
                                                            <MenuItem value={'t1'}>Tenant 1</MenuItem>
                                                            <MenuItem value={'t2'}>Tenant 2</MenuItem>
                                                            <MenuItem value={'t3'}>Tenant 3</MenuItem>
                                                        </Select>
                                                        <FormHelperText>{form.errors.tenantId?.toString()}</FormHelperText>
                                                    </FormControl>

                                                    <FormControl fullWidth variant="outlined">
                                                        <InputLabel id="user-label">User</InputLabel>
                                                        <Select
                                                            labelId="user-label"
                                                            id="user"
                                                            label="User"
                                                            {...form.getFieldProps('userId')}
                                                            error={form.errors.userId !== undefined}
                                                        >
                                                            <MenuItem value="">
                                                                <em>None</em>
                                                            </MenuItem>
                                                            <MenuItem value={'t1'}>User 1</MenuItem>
                                                            <MenuItem value={'t2'}>User 2</MenuItem>
                                                            <MenuItem value={'t3'}>User 3</MenuItem>
                                                        </Select>
                                                        <FormHelperText>{form.errors.userId?.toString()}</FormHelperText>
                                                    </FormControl>
                                                </Stack>
                                            </Grid>
                                            <Grid size={{xs: 12, md: 6}}>
                                                <Typography variant="h6" align="center" gutterBottom>API Client
                                                    Scopes</Typography>
                                            </Grid>
                                        </Grid>
                                    </>
                                )}
                            </DialogContent>
                            <DialogActions>
                                <Button variant="contained" color="error" type="reset"
                                        onClick={closeDialog}>{isValid ? 'Cancel' : 'Close'}</Button>
                                {isValid && (
                                    <Button variant="contained"
                                            type="submit">{isEdit ? 'Update' : 'Create'} API Client</Button>
                                )}

                            </DialogActions>
                        </form>
                    )}
                </Formik>
            </Dialog>
        </React.Fragment>
    );
}

export default FormDialog;