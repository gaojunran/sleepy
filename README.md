# Sleepy

睡着了嘛😴？在干嘛？

Sleepy可以记录你的设备状态（手机电量，前台应用……），并实时展示在页面上。

本项目创意来自B站视频[改了个能让各位实时视奸我的网站](https://b23.tv/aHAUFFo)，使用Vue3 + Supabase重构实现。

![Screenshot](<./public/Screenshot.png>)

## 如何使用

### 在线使用

访问[https://sleepy-nebula.netlify.app/].

### 使用Netlify和Supabase自部署

如果你想借助我的源码构建一个自己的网站，可遵照以下步骤：

#### **STEP 1** 在Supabase中新建一个项目

创建一个名为`records`的数据库，开启`RLS`认证。

建表语句如下：

```sql
create table public.records (
  id bigint generated by default as identity not null,
  updated_at timestamp with time zone not null default now(),
  source smallint not null default '-1'::smallint,
  battery smallint not null default '-1'::smallint,
  app text null,
  constraint records_pkey primary key (id),
  constraint records_id_key unique (id)
) TABLESPACE pg_default;
```

Policy配置如下：（您也可以配置更细粒度的权限）

```sql
alter policy "Enable access for all users"
on "public"."records"
to public
using (
  true
);
```

#### **STEP 2** 在Netlify中部署本项目。

本项目配置已在[./netlify.toml](./netlify.toml)中设置好；你需要在Netlify中配置与Supabase相关的环境变量，如下：

```ini
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

#### **STEP 3** 在MacroDroid中配置触发器。

当触发器为「应用程序打开（所有应用程序）」时，触发动作，发送以下HTTP请求：

```bash
curl --location --request POST '<VITE_SUPABASE_URL>/rest/v1/records' \
--header 'apikey: <VITE_SUPABASE_ANON_KEY>' \
--header 'Authorization: Bearer <VITE_SUPABASE_ANON_KEY>' \
--header 'Prefer: return=minimal' \
--header 'Content-Type: application/json' \
--data-raw '{"battery": "{battery}", "source": "1", "app": "{fg_app_name}"}'
```

其中尖括号内的内容需要您进行动态替换。`{battery}`和`{fg_app_name}`分别表示当前设备电量以及前台应用名称，可在MacroDroid中通过这样的大括号插值形式获取。

注意，您需要给MacroDroid提供**无障碍权限和「无限制」的省电配置**，否则可能无法获取最及时的消息。

<!-- #### **STEP 4** 在Netlify中部署本项目。

TODO -->

## 其它

本项目使用[Vitesse Lite](https://github.com/antfu/vitesse-lite)作为模板。
