import React from 'react'
import { Layout, Menu, Typography } from 'antd'
import {
  FileTextOutlined,
  UserOutlined,
  PictureOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons'
import ScriptEditor from './components/ScriptEditor'
import CharacterManager from './components/CharacterManager'
import SceneManager from './components/SceneManager'
import VideoGenerator from './components/VideoGenerator'

const { Header, Sider, Content } = Layout
const { Title } = Typography

function App() {
  const [selectedKey, setSelectedKey] = React.useState('script')

  const menuItems = [
    {
      key: 'script',
      icon: <FileTextOutlined />,
      label: '剧本编辑',
    },
    {
      key: 'characters',
      icon: <UserOutlined />,
      label: '角色管理',
    },
    {
      key: 'scenes',
      icon: <PictureOutlined />,
      label: '场景管理',
    },
    {
      key: 'video',
      icon: <VideoCameraOutlined />,
      label: '视频生成',
    },
  ]

  const renderContent = () => {
    switch (selectedKey) {
      case 'script':
        return <ScriptEditor />
      case 'characters':
        return <CharacterManager />
      case 'scenes':
        return <SceneManager />
      case 'video':
        return <VideoGenerator />
      default:
        return <ScriptEditor />
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: '0 24px', background: '#001529' }}>
        <Title level={3} style={{ color: 'white', margin: '16px 0' }}>
          AI视频生成工具
        </Title>
      </Header>
      <Layout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
            onClick={({ key }) => setSelectedKey(key)}
          />
        </Sider>
        <Layout style={{ padding: '0 24px 24px' }}>
          <Content
            style={{
              background: '#fff',
              padding: 24,
              margin: 0,
              minHeight: 280,
              borderRadius: 8,
            }}
          >
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  )
}

export default App
