import React, { useState } from 'react'
import {
  Card,
  Input,
  Button,
  message,
  Typography,
  Space,
  Row,
  Col,
  Image,
  List,
  Tag,
} from 'antd'
import {
  PictureOutlined,
  PlusOutlined,
  DeleteOutlined,
  EyeOutlined,
} from '@ant-design/icons'
import { generateScene } from '../services/api'

const { Title, Paragraph } = Typography
const { TextArea } = Input

interface Scene {
  id: string
  name: string
  description: string
  imageUrl?: string
  mood?: string
  timeOfDay?: string
}

const SceneManager: React.FC = () => {
  const [scenes, setScenes] = useState<Scene[]>([])
  const [newSceneDesc, setNewSceneDesc] = useState('')
  const [loading, setLoading] = useState(false)

  const handleGenerateScene = async () => {
    if (!newSceneDesc.trim()) {
      message.warning('请输入场景描述')
      return
    }

    setLoading(true)
    try {
      const result = await generateScene(newSceneDesc)

      const newScene: Scene = {
        id: Date.now().toString(),
        name: result.name || '新场景',
        description: newSceneDesc,
        imageUrl: result.image_url,
        mood: result.mood,
        timeOfDay: result.time_of_day,
      }

      setScenes([...scenes, newScene])
      setNewSceneDesc('')
      message.success('场景生成成功！')
    } catch (error) {
      console.error('生成场景失败:', error)
      message.error('生成场景失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteScene = (id: string) => {
    setScenes(scenes.filter((scene) => scene.id !== id))
    message.success('场景已删除')
  }

  const sceneExamples = [
    '温馨的咖啡厅，下午阳光透过窗户洒在桌上',
    '夜晚的城市街道，霓虹灯闪烁',
    '宁静的海边，夕阳西下',
    '现代化的办公室，明亮整洁',
    '古典的图书馆，书香四溢',
  ]

  return (
    <div>
      <Title level={2}>
        <PictureOutlined /> 场景管理
      </Title>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={12}>
          <Card title="创建新场景" extra={<PlusOutlined />}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Paragraph>场景描述</Paragraph>
                <TextArea
                  value={newSceneDesc}
                  onChange={(e) => setNewSceneDesc(e.target.value)}
                  placeholder="请描述场景的环境、氛围、时间等，例如：温馨的餐厅，晚上，浪漫氛围"
                  rows={4}
                />
              </div>

              <div>
                <Paragraph>示例场景</Paragraph>
                <Space wrap>
                  {sceneExamples.map((example, index) => (
                    <Tag
                      key={index}
                      style={{ cursor: 'pointer' }}
                      onClick={() => setNewSceneDesc(example)}
                    >
                      {example}
                    </Tag>
                  ))}
                </Space>
              </div>

              <Button
                type="primary"
                onClick={handleGenerateScene}
                loading={loading}
                size="large"
                block
              >
                生成场景
              </Button>
            </Space>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title={`场景列表 (${scenes.length})`}>
            {scenes.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px 0' }}>
                <PictureOutlined style={{ fontSize: '48px', color: '#d9d9d9' }} />
                <Paragraph type="secondary">暂无场景，请先创建场景</Paragraph>
              </div>
            ) : (
              <List
                dataSource={scenes}
                renderItem={(scene) => (
                  <List.Item
                    actions={[
                      scene.imageUrl && (
                        <Button
                          key="preview"
                          type="text"
                          icon={<EyeOutlined />}
                          onClick={() => {
                            // 预览图片
                            window.open(scene.imageUrl, '_blank')
                          }}
                        >
                          预览
                        </Button>
                      ),
                      <Button
                        key="delete"
                        type="text"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={() => handleDeleteScene(scene.id)}
                      >
                        删除
                      </Button>,
                    ].filter(Boolean)}
                  >
                    <List.Item.Meta
                      avatar={
                        scene.imageUrl ? (
                          <Image
                            src={scene.imageUrl}
                            width={80}
                            height={60}
                            style={{ borderRadius: '4px', objectFit: 'cover' }}
                            fallback="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAADDCAYAAADQvc6UAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJFjYGASSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8LAwSDCIMogwMCcmFxc4BgQ4ANUwgCjUcG3awyMIPqyLsis7PPOq3QdDFcvjV3jOD1boQVTPQrgSkktTgbSf4A4LbmgqISBgTEFyFYuLykAsTuAbJEioKOA7DkgdjqEvQHEToKwj4DVhAQ5A9k3gGyB5IxEoBmML4BsnSQk8XQkNtReEOBxcfXxUQg1Mjc0dyHgXNJBSWpFCYh2zi+oLMpMzyhRcASGUqqCZ16yno6CkYGRAQMDKMwhqj/fAIcloxgHQqxAjIHBEugw5sUIsSQpBobtQPdLciLEVJYzMPBHMDBsayhILEqEO4DxG0txmrERhM29nYGBddr//5/DGRjYNRkY/l7////39v///y4Dmn+LgeHANwDrkl1AuO+pmgAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAwqADAAQAAAABAAAAwwAAAAD9b/HnAAAHlklEQVR4Ae3dP3Ik1RnG4W+FgYxN"
                          />
                        ) : (
                          <div
                            style={{
                              width: 80,
                              height: 60,
                              backgroundColor: '#f0f0f0',
                              borderRadius: '4px',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}
                          >
                            <PictureOutlined style={{ color: '#d9d9d9' }} />
                          </div>
                        )
                      }
                      title={scene.name}
                      description={
                        <div>
                          <Paragraph ellipsis={{ rows: 2 }}>
                            {scene.description}
                          </Paragraph>
                          <Space>
                            {scene.mood && <Tag color="blue">{scene.mood}</Tag>}
                            {scene.timeOfDay && <Tag color="orange">{scene.timeOfDay}</Tag>}
                          </Space>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default SceneManager