import * as React from 'react';
import {useFormik, Formik, FormikHelpers, FormikValues} from 'formik';
import {object, string, ObjectSchema} from 'yup';
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

} from '@mui/material';
import {IRecordFormMode} from '@app/types/service';
import {IUser} from '@app/types/system/users';

type FormDialogProps = {
    open: boolean;
    mode: 'create' | 'update';
    initialValues?: IUser;
    onSubmit: (form: FormikHelpers<IUser>, values: IUser) => Promise<void>;
    onCancel: () => void;
};

interface formRequirements {
    usernameRequired: boolean;
    usernameMinLength: number;
    usernameMaxLength: number;
    passwordRequired: boolean;
    passwordMinLength: number;
    passwordMaxLength: number;
    emailRequired: boolean;
    emailMinLength: number;
    emailMaxLength: number;
    phoneRequired: boolean;
    phoneMinLength: number;
    phoneMaxLength: number;
    statusRequired: boolean;
    tenantIdRequired: boolean;
    tenantIdLength: number;
}

const formReqs: formRequirements = {
    usernameRequired: true,
    usernameMinLength: 4,
    usernameMaxLength: 100,
    passwordRequired: true,
    passwordMinLength: 4,
    passwordMaxLength: 100,
    emailRequired: true,
    emailMinLength: 3,
    emailMaxLength: 100,
    phoneRequired: false,
    phoneMinLength: 7,
    phoneMaxLength: 15,
    statusRequired: true,
    tenantIdRequired: false,
    tenantIdLength: 32,
};

const getValidationSchema = (mode: IRecordFormMode) => {
    const schema = {
        username: string()
            .required('Username is required.')
            .min(formReqs.usernameMinLength, `Username must be at least ${formReqs.usernameMinLength} characters.`)
            .max(formReqs.usernameMaxLength, `Username must be at most ${formReqs.usernameMaxLength} characters.`),
        password: string()
            .min(formReqs.passwordMinLength, `Password must be at least ${formReqs.passwordMinLength} characters.`)
            .max(formReqs.passwordMaxLength, `Password must be at most ${formReqs.passwordMaxLength} characters.`),
        email: string()
            .required('Email is required.')
            .email('A valid email address is required.')
            .min(formReqs.emailMinLength, `Email must be at least ${formReqs.emailMinLength} characters.`)
            .max(formReqs.emailMaxLength, `Email must be at most ${formReqs.emailMaxLength} characters.`),
        phoneNumber: string().nullable()
            .min(formReqs.phoneMinLength, `Phone Number must be at least ${formReqs.phoneMinLength} digits.`)
            .max(formReqs.phoneMaxLength, `Phone Number must be at most ${formReqs.phoneMaxLength} digits.`),
        status: string()
            .required('Status is required.'),
        tenantId: string()
            .length(formReqs.tenantIdLength, 'Tenant ID is not valid.'),
    };

    if (mode === 'create') {
        schema.password = schema.password.required('Password is required.');
    }

    return object(schema);
};

export const FormDialog: React.FC<FormDialogProps> = ({open, mode, initialValues, onSubmit, onCancel}) => {
    return (
        <React.Fragment>
            <Dialog
                fullWidth={true}
                maxWidth={'md'}
                open={open}
                onClose={() => onCancel()}
            >
                <Formik
                    initialValues={initialValues! as FormikValues}
                    validationSchema={getValidationSchema(mode)}
                    enableReinitialize={true}
                    validateOnChange={false}
                    validateOnBlur={false}
                    onSubmit={async (values, actions) => onSubmit(actions as FormikHelpers<IUser>, values as IUser)}
                >
                    {form => (
                        <form onSubmit={form.handleSubmit} onReset={form.handleReset}>
                            <DialogTitle>{mode === 'create' ? 'Create' : 'Update'} User</DialogTitle>
                            <DialogContent>
                                <DialogContentText>
                                    <Typography variant="body1">Please provide the following details to create a new
                                        user
                                        and
                                        then click Save once finished.</Typography>
                                    {form.status && (
                                        <>
                                            <Typography variant="body1" color="error"
                                                        className="formStatus">{form.status}</Typography>
                                        </>
                                    )}
                                </DialogContentText>
                                <Grid container marginY={2}>
                                    <Grid size={{xs: 12, md: 6}}>
                                        <Typography variant="h6" align="center" gutterBottom>User
                                            Information</Typography>
                                        <Stack component="form" spacing={3} noValidate>
                                            <TextField
                                                label="Username"
                                                variant="outlined" // Common variant for forms
                                                fullWidth
                                                {...form.getFieldProps('username')}
                                                error={form.errors.username !== undefined}
                                                helperText={form.errors.username?.toString()}
                                            />

                                            <TextField
                                                label="Password"
                                                type="password" // Masks the input for security
                                                variant="outlined"
                                                fullWidth
                                                {...form.getFieldProps('password')}
                                                error={form.errors.password !== undefined}
                                                helperText={form.errors.password?.toString()}
                                            />

                                            <TextField
                                                label="Email"
                                                type="email" // Ensures correct keyboard type on mobile and basic validation
                                                variant="outlined"
                                                fullWidth
                                                {...form.getFieldProps('email')}
                                                error={form.errors.email !== undefined}
                                                helperText={form.errors.email?.toString()}
                                            />

                                            <TextField
                                                label="Phone Number"
                                                type="tel" // Ensures correct keyboard type on mobile and basic validation
                                                variant="outlined"
                                                fullWidth
                                                {...form.getFieldProps('phoneNumber')}
                                                error={form.errors.phoneNumber !== undefined}
                                                helperText={form.errors.phoneNumber?.toString()}
                                            />

                                            <FormControl fullWidth variant="outlined">
                                                <InputLabel id="status-label">Status</InputLabel>
                                                <Select
                                                    labelId="status-label"
                                                    id="status"
                                                    label="Status"
                                                    {...form.getFieldProps('status')}
                                                    error={form.errors.status !== undefined}
                                                >
                                                    <MenuItem value="">
                                                        <em>None</em>
                                                    </MenuItem>
                                                    <MenuItem value={'pending'}>Pending</MenuItem>
                                                    <MenuItem value={'invited'}>Invited</MenuItem>
                                                    <MenuItem value={'active'}>Active</MenuItem>
                                                    <MenuItem value={'suspended'}>Suspended</MenuItem>
                                                    <MenuItem value={'disabled'}>Disabled</MenuItem>
                                                </Select>
                                                <FormHelperText>{form.errors.status?.toString()}</FormHelperText>
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
                                        </Stack>
                                    </Grid>
                                    <Grid size={{xs: 12, md: 6}}>
                                        <Typography variant="h6" align="center" gutterBottom>User Roles</Typography>
                                    </Grid>
                                </Grid>
                            </DialogContent>
                            <DialogActions>
                                <Button variant="contained" color="error" type="reset"
                                        onClick={() => onCancel()}>Cancel</Button>
                                <Button variant="contained"
                                        type="submit">{mode === 'create' ? 'Create' : 'Update'} User</Button>
                            </DialogActions>
                        </form>
                    )}
                </Formik>
            </Dialog>
        </React.Fragment>
    );
}

export default FormDialog;