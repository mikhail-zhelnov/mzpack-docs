import React, {memo} from 'react';
import {useThemeConfig} from '@docusaurus/theme-common';
import {groupBlogSidebarItemsByYear} from '@docusaurus/plugin-content-blog/client';
import Heading from '@theme/Heading';

function BlogSidebarYearGroup({
  year,
  yearGroupHeadingClassName,
  children,
  defaultOpen,
}: {
  year: string;
  yearGroupHeadingClassName?: string;
  children: React.ReactNode;
  defaultOpen: boolean;
}) {
  return (
    <details open={defaultOpen || undefined} className="blog-year-group">
      <summary className={yearGroupHeadingClassName}>
        <Heading as="h3" style={{display: 'inline', cursor: 'pointer'}}>
          {year}
        </Heading>
      </summary>
      {children}
    </details>
  );
}

function BlogSidebarContent({
  items,
  yearGroupHeadingClassName,
  ListComponent,
}: {
  items: readonly {readonly date: string; readonly title: string; readonly permalink: string}[];
  yearGroupHeadingClassName?: string;
  ListComponent: React.ComponentType<{items: typeof items}>;
}) {
  const themeConfig = useThemeConfig();
  if ((themeConfig as any).blog?.sidebar?.groupByYear) {
    const itemsByYear = groupBlogSidebarItemsByYear(items);
    return (
      <>
        {itemsByYear.map(([year, yearItems], index) => (
          <BlogSidebarYearGroup
            key={year}
            year={year}
            yearGroupHeadingClassName={yearGroupHeadingClassName}
            defaultOpen={index === 0}>
            <ListComponent items={yearItems} />
          </BlogSidebarYearGroup>
        ))}
      </>
    );
  } else {
    return <ListComponent items={items} />;
  }
}

export default memo(BlogSidebarContent);
