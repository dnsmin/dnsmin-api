import * as React from 'react';
import {useEffect, useRef} from 'react';
import {PageTitleProps} from '@app/types/window';

function useDocumentTitle(title: string, prevailOnUnmount: boolean = false) {
    const defaultTitle = useRef(document.title);

    useEffect(() => {
        document.title = title;
    }, [title]);

    useEffect(
        () => () => {
            if (!prevailOnUnmount) {
                document.title = defaultTitle.current;
            }
        },
        []
    );
}

export const PageTitle: React.FC<PageTitleProps> = ({title, children}) => {
    const titlePrefix = "DNSMin | ";
    useDocumentTitle(`${titlePrefix}${title}`);
    return children;
}

export default PageTitle;