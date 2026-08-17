from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, auth, database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_task = models.Task(
        **task.model_dump(),
        owner_id=current_user.id,
        status="open"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("", response_model=List[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
        
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task_query = db.query(models.Task).filter(models.Task.id == task_id)
    task = task_query.first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
        
    # Partial update: only update provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    
    if update_data:
        task_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(task)
        
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task_query = db.query(models.Task).filter(models.Task.id == task_id)
    task = task_query.first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
        
    task_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Task deleted successfully"}
