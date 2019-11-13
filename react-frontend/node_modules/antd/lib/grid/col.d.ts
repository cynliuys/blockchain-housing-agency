import * as React from 'react';
import * as PropTypes from 'prop-types';
import { ConfigConsumerProps } from '../config-provider';
export interface ColSize {
    span?: number;
    order?: number;
    offset?: number;
    push?: number;
    pull?: number;
}
export interface ColProps extends React.HTMLAttributes<HTMLDivElement> {
    span?: number;
    order?: number;
    offset?: number;
    push?: number;
    pull?: number;
    xs?: number | ColSize;
    sm?: number | ColSize;
    md?: number | ColSize;
    lg?: number | ColSize;
    xl?: number | ColSize;
    xxl?: number | ColSize;
    prefixCls?: string;
}
export default class Col extends React.Component<ColProps, {}> {
    static propTypes: {
        span: PropTypes.Requireable<number>;
        order: PropTypes.Requireable<number>;
        offset: PropTypes.Requireable<number>;
        push: PropTypes.Requireable<number>;
        pull: PropTypes.Requireable<number>;
        className: PropTypes.Requireable<string>;
        children: PropTypes.Requireable<PropTypes.ReactNodeLike>;
        xs: PropTypes.Requireable<number | object>;
        sm: PropTypes.Requireable<number | object>;
        md: PropTypes.Requireable<number | object>;
        lg: PropTypes.Requireable<number | object>;
        xl: PropTypes.Requireable<number | object>;
        xxl: PropTypes.Requireable<number | object>;
    };
    renderCol: ({ getPrefixCls }: ConfigConsumerProps) => JSX.Element;
    render(): JSX.Element;
}
