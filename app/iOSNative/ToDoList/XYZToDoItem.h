//
//  XYZToDoItem.h
//  ToDoList
//
//  Created by chen hengjie on 1/4/14.
//  Copyright (c) 2014 chen hengjie. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface XYZToDoItem : NSObject

@property NSString *itemName;
@property BOOL completed;
@property (readonly) NSDate *creationDate;

@end
