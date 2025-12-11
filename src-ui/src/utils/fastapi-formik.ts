export function mapFastApiErrorsToFormik(detail: any[]): Record<string, string> {
    const formikErrors: Record<string, string> = {};
    for (const err of detail) {
        const field = err.loc[1];
        formikErrors[field] = err.msg;
    }
    return formikErrors;
}