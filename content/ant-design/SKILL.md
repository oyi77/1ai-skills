---
name: ant-design
description: Ant Design React component library — enterprise UI, forms, tables, charts, theming, ProComponents
---

## Overview

Ant Design is an enterprise-grade React UI library with 60+ components, a design system, and ProComponents for advanced business scenarios. Widely used for admin dashboards, CMS, and data-heavy applications.

## Capabilities

- 60+ polished components with consistent design language
- ConfigProvider for global theming (colors, locale, prefixCls)
- Form component with validation, dependencies, dynamic fields
- Table with sorting, filtering, pagination, virtual scroll
- ProComponents: ProTable, ProForm, ProLayout, ProDescriptions
- Day.js integration for date components
- Ant Design Icons (300+)

## When to Use

- Building enterprise admin dashboards and CMS
- Need advanced form handling with complex validation
- Want a complete design system with minimal customization
- Building data-heavy applications with tables, charts, filters

## Pseudo Code

### Installation
```bash
npm install antd @ant-design/icons
# ProComponents for advanced patterns
npm install @ant-design/pro-components
```

### Theme Configuration
```tsx
import { ConfigProvider } from "antd"

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1677ff",
          borderRadius: 6,
          fontFamily: "Inter, sans-serif",
        },
      }}
    >
      <YourApp />
    </ConfigProvider>
  )
}
```

### Form with Validation
```tsx
import { Form, Input, Select, Button, message } from "antd"

export function UserForm() {
  const [form] = Form.useForm()
  const onFinish = (values) => {
    message.success("Saved!")
    console.log(values)
  }

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item name="name" label="Name" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="role" label="Role" rules={[{ required: true }]}>
        <Select options={[{ value: "admin" }, { value: "user" }]} />
      </Form.Item>
      <Button type="primary" htmlType="submit">Save</Button>
    </Form>
  )
}
```

### ProTable
```tsx
import { ProTable } from "@ant-design/pro-components"

const columns = [
  { title: "Name", dataIndex: "name", sorter: true },
  { title: "Status", dataIndex: "status", valueEnum: { active: "Active", inactive: "Inactive" } },
  { title: "Created", dataIndex: "createdAt", valueType: "date" },
]

export function UserTable() {
  return (
    <ProTable
      columns={columns}
      request={async (params) => {
        const data = await fetchUsers(params)
        return { data: data.list, total: data.total }
      }}
      search={{ labelWidth: "auto" }}
      pagination={{ pageSize: 20 }}
    />
  )
}
```

## Common Patterns

- **ConfigProvider locale**: `<ConfigProvider locale={zhCN}>` for i18n
- **Form dependencies**: `shouldUpdate={(prev, cur) => prev.field !== cur.field}` for conditional fields
- **Table virtual scroll**: `virtual` prop for 1000+ row performance
- **message/notification**: `message.success()`, `notification.error()` for feedback
- **Responsive Grid**: `<Row gutter={[16, 16]}><Col xs={24} md={12}>...</Col></Row>`
