import React, { useState } from 'react'
import {
  Card,
  Input,
  Button,
  Upload,
  message,
  Typography,
  Space,
  Row,
  Col,
  Image,
  List,
  Avatar,
} from 'antd'
import {
  UserOutlined,
  PlusOutlined,
  UploadOutlined,
  DeleteOutlined,
} from '@ant-design/icons'
import { generateCharacter, generateCharacterWithImage } from '../services/api'

const { Title, Paragraph } = Typography
const { TextArea } = Input

interface Character {
  id: string
  name: string
  description: string
  imageUrl?: string
  voiceModel?: string
}

const CharacterManager: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([])
  const [newCharacterDesc, setNewCharacterDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploadFile, setUploadFile] = useState<File | null>(null)

  const handleGenerateCharacter = async () => {
    if (!newCharacterDesc.trim()) {
      message.warning('请输入角色描述')
      return
    }

    setLoading(true)
    try {
      let result
      if (uploadFile) {
        result = await generateCharacterWithImage(newCharacterDesc, uploadFile)
      } else {
        result = await generateCharacter(newCharacterDesc)
      }

      const newCharacter: Character = {
        id: Date.now().toString(),
        name: result.name || '新角色',
        description: newCharacterDesc,
        imageUrl: result.image_url,
        voiceModel: result.voice_model,
      }

      setCharacters([...characters, newCharacter])
      setNewCharacterDesc('')
      setUploadFile(null)
      message.success('角色生成成功！')
    } catch (error) {
      console.error('生成角色失败:', error)
      message.error('生成角色失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteCharacter = (id: string) => {
    setCharacters(characters.filter((char) => char.id !== id))
    message.success('角色已删除')
  }

  const uploadProps = {
    beforeUpload: (file: File) => {
      const isImage = file.type.startsWith('image/')
      if (!isImage) {
        message.error('只能上传图片文件！')
        return false
      }
      const isLt5M = file.size / 1024 / 1024 < 5
      if (!isLt5M) {
        message.error('图片大小不能超过5MB！')
        return false
      }
      setUploadFile(file)
      return false // 阻止自动上传
    },
    onRemove: () => {
      setUploadFile(null)
    },
    fileList: uploadFile ? [uploadFile as any] : [],
  }

  return (
    <div>
      <Title level={2}>
        <UserOutlined /> 角色管理
      </Title>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={12}>
          <Card title="创建新角色" extra={<PlusOutlined />}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Paragraph>角色描述</Paragraph>
                <TextArea
                  value={newCharacterDesc}
                  onChange={(e) => setNewCharacterDesc(e.target.value)}
                  placeholder="请描述角色的外貌、性格、服装等特征，例如：25岁男性，温文尔雅，穿着白色衬衫"
                  rows={4}
                />
              </div>

              <div>
                <Paragraph>参考图片（可选）</Paragraph>
                <Upload {...uploadProps}>
                  <Button icon={<UploadOutlined />}>选择图片</Button>
                </Upload>
                <Paragraph type="secondary" style={{ fontSize: '12px', marginTop: 8 }}>
                  上传角色参考图片，AI将基于此图片生成相似角色
                </Paragraph>
              </div>

              <Button
                type="primary"
                onClick={handleGenerateCharacter}
                loading={loading}
                size="large"
                block
              >
                生成角色
              </Button>
            </Space>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title={`角色列表 (${characters.length})`}>
            {characters.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px 0' }}>
                <UserOutlined style={{ fontSize: '48px', color: '#d9d9d9' }} />
                <Paragraph type="secondary">暂无角色，请先创建角色</Paragraph>
              </div>
            ) : (
              <List
                dataSource={characters}
                renderItem={(character) => (
                  <List.Item
                    actions={[
                      <Button
                        key="delete"
                        type="text"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={() => handleDeleteCharacter(character.id)}
                      >
                        删除
                      </Button>,
                    ]}
                  >
                    <List.Item.Meta
                      avatar={
                        character.imageUrl ? (
                          <Image
                            src={character.imageUrl}
                            width={64}
                            height={64}
                            style={{ borderRadius: '50%', objectFit: 'cover' }}
                            fallback="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAADDCAYAAADQvc6UAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJFjYGASSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8LAwSDCIMogwMCcmFxc4BgQ4ANUwgCjUcG3awyMIPqyLsis7PPOq3QdDFcvjV3jOD1boQVTPQrgSkktTgbSf4A4LbmgqISBgTEFyFYuLykAsTuAbJEioKOA7DkgdjqEvQHEToKwj4DVhAQ5A9k3gGyB5IxEoBmML4BsnSQk8XQkNtReEOBxcfXxUQg1Mjc0dyHgXNJBSWpFCYh2zi+oLMpMzyhRcASGUqqCZ16yno6CkYGRAQMDKMwhqj/fAIcloxgHQqxAjIHBEugw5sUIsSQpBobtQPdLciLEVJYzMPBHMDBsayhILEqEO4DxG0txmrERhM29nYGBddr//5/DGRjYNRkY/l7////39v///y4Dmn+LgeHANwDrkl1AuO+pmgAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAwqADAAQAAAABAAAAwwAAAAD9b/HnAAAHlklEQVR4Ae3dP3Ik1RnG4W+FgYxN"
                          />
                        ) : (
                          <Avatar size={64} icon={<UserOutlined />} />
                        )
                      }
                      title={character.name}
                      description={
                        <div>
                          <Paragraph ellipsis={{ rows: 2 }}>
                            {character.description}
                          </Paragraph>
                          {character.voiceModel && (
                            <Paragraph type="secondary" style={{ fontSize: '12px' }}>
                              语音模型: {character.voiceModel}
                            </Paragraph>
                          )}
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

export default CharacterManager