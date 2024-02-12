from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from datetime import datetime
from typing import Optional

from api.quiz.question.models import QuestionBank, QuestionBankReadWithOptions
from api.quiz.quiz.link_models import QuizTopic



class ContentBase(SQLModel):
    
    topic_id: int | None = Field(foreign_key='topic.id', default=None, index=True)
    content_text: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic_id": 1,
                "content_text": "This is the content of the topic"
            }
        }

class Content(ContentBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))
    
    # Topic Relationship
    topic: "Topic" = Relationship(back_populates='contents') # type: ignore


class ContentCreate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ContentUpdate(ContentBase):
    topic_id: int | None = None
    content_text: str | None = None


class TopicBase(SQLModel):
    title: str = Field(max_length=160, index=True)
    description: str
    parent_id: int | None = Field(
        foreign_key='topic.id',  # notice the lowercase "t" to refer to the database table name
        default=None    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOP Paradigm",
                "description": "Learn OOPS in Typescript 5.0+",
                "parent_id": 1 # This is Optional for Subtopics
            }
        }

# It will include Topics, Subtopics, CaseStudies Given for Assessments
class Topic(TopicBase, table=True):

    id: int | None = Field(default=None, primary_key=True, index=True)

    children_topics: list['Topic'] = Relationship(back_populates='parent_topic')
    parent_topic: Optional['Topic'] = Relationship(
        back_populates='children_topics',
        sa_relationship_kwargs=dict(
            remote_side='Topic.id'  # notice the uppercase "T" to refer to this table class
        )
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(
            DateTime(timezone=True),
            onupdate=datetime.utcnow,
            nullable=False,
        ))

    # QuestionBank Relationship
    questions: list['QuestionBank'] = Relationship(
        back_populates='topic', sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # Content Table relationship to store the content of the topic
    contents: list['Content'] = Relationship(back_populates='topic', sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    # Relationship with QuizTopic
    quizzes: list['api.quiz.quiz.models.Quiz'] = Relationship(back_populates="topics", link_model=QuizTopic)


class TopicCreate(TopicBase):
    # pass
    contents: list['ContentCreate'] = []

    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOP Paradigm",
                "description": "Learn OOPS in Typescript 5.0+",
                "parent_id": 1, # This is Optional for Subtopics
                "contents": [
                    {"content_text": "OOP is a programming paradigm based on classes and objects rather."},
                    {"content_text": "OOP Pillars: Encapsulation, Inheritance and Polymorphism, and Abstraction."}
                ]
            }
        }


class TopicResponse(TopicBase):
    id: int
    parent_id: int | None = None
    created_at: datetime
    updated_at: datetime


class TopicUpdate(TopicBase):
    title: str | None = None
    description: str | None = None
    parent_id: int | None = None


    class Config:
        json_schema_extra = {
            "example": {
                "title": "OOP Paradigm",
                "description": "Learn OOPS in Typescript 5.0+",
                "parent_id": 1 # This is Optional for Subtopics
            }
        }

class TopicResponseWithContent(TopicResponse):
    contents: list['ContentResponse'] = []

class TopicResponseWithQuestions(TopicResponse):
    questions: list[QuestionBankReadWithOptions] = []