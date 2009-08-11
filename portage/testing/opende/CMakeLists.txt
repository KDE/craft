project(opende)

cmake_minimum_required(VERSION 2.6)

configure_file(${CMAKE_SOURCE_DIR}/build/config-default.h ${CMAKE_BINARY_DIR}/config.h)

add_definitions(-DODE_DLL)

include_directories(${CMAKE_BINARY_DIR} ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/opcode)


set (OPCODE_SOURCES 
    OPCODE/OPC_AABBCollider.cpp    
    OPCODE/OPC_AABBCollider.h
    OPCODE/OPC_AABBTree.cpp        
    OPCODE/OPC_AABBTree.h
    OPCODE/OPC_BaseModel.cpp       
    OPCODE/OPC_BaseModel.h
    OPCODE/OPC_Collider.cpp        
    OPCODE/OPC_Collider.h
    OPCODE/OPC_Common.cpp          
    OPCODE/OPC_Common.h
    OPCODE/OPC_HybridModel.cpp     
    OPCODE/OPC_HybridModel.h
    OPCODE/OPC_LSSCollider.cpp     
    OPCODE/OPC_LSSCollider.h
    OPCODE/OPC_MeshInterface.cpp   
    OPCODE/OPC_MeshInterface.h
    OPCODE/OPC_Model.cpp           
    OPCODE/OPC_Model.h
    OPCODE/OPC_OBBCollider.cpp     
    OPCODE/OPC_OBBCollider.h
    OPCODE/Opcode.cpp              
    OPCODE/Opcode.h
    OPCODE/OPC_OptimizedTree.cpp   
    OPCODE/OPC_OptimizedTree.h
    OPCODE/OPC_Picking.cpp         
    OPCODE/OPC_Picking.h
    OPCODE/OPC_PlanesCollider.cpp  
    OPCODE/OPC_PlanesCollider.h
    OPCODE/OPC_RayCollider.cpp     
    OPCODE/OPC_RayCollider.h
    OPCODE/OPC_SphereCollider.cpp  
    OPCODE/OPC_SphereCollider.h
    OPCODE/OPC_TreeBuilders.cpp    
    OPCODE/OPC_TreeBuilders.h
    OPCODE/OPC_TreeCollider.cpp    
    OPCODE/OPC_TreeCollider.h
    OPCODE/OPC_VolumeCollider.cpp  
    OPCODE/OPC_VolumeCollider.h
    OPCODE/OPC_Settings.h
    OPCODE/OPC_SphereAABBOverlap.h
    OPCODE/OPC_BoxBoxOverlap.h
    OPCODE/OPC_SphereTriOverlap.h
    OPCODE/OPC_PlanesAABBOverlap.h
    OPCODE/OPC_TriBoxOverlap.h
    OPCODE/OPC_IceHook.h
    OPCODE/OPC_PlanesTriOverlap.h
    OPCODE/OPC_TriTriOverlap.h
    OPCODE/OPC_LSSAABBOverlap.h
    OPCODE/OPC_RayAABBOverlap.h
    OPCODE/Stdafx.h
    OPCODE/OPC_LSSTriOverlap.h
    OPCODE/OPC_RayTriOverlap.h 
)

set (OPCODE_ICE_SOURCES
    OPCODE/Ice/IceAABB.cpp             
    OPCODE/Ice/IceAABB.h             
    OPCODE/Ice/IceAxes.h
    OPCODE/Ice/IceBoundingSphere.h     
    OPCODE/Ice/IceContainer.cpp      
    OPCODE/Ice/IceContainer.h
    OPCODE/Ice/IceFPU.h                
    OPCODE/Ice/IceHPoint.cpp         
    OPCODE/Ice/IceHPoint.h
    OPCODE/Ice/IceIndexedTriangle.cpp  
    OPCODE/Ice/IceIndexedTriangle.h  
    OPCODE/Ice/IceLSS.h
    OPCODE/Ice/IceMatrix3x3.cpp        
    OPCODE/Ice/IceMatrix3x3.h        
    OPCODE/Ice/IceMatrix4x4.cpp
    OPCODE/Ice/IceMatrix4x4.h          
    OPCODE/Ice/IceMemoryMacros.h     
    OPCODE/Ice/IceOBB.cpp
    OPCODE/Ice/IceOBB.h                
    OPCODE/Ice/IcePairs.h            
    OPCODE/Ice/IcePlane.cpp
    OPCODE/Ice/IcePlane.h              
    OPCODE/Ice/IcePoint.cpp          
    OPCODE/Ice/IcePoint.h
    OPCODE/Ice/IcePreprocessor.h       
    OPCODE/Ice/IceRandom.cpp         
    OPCODE/Ice/IceRandom.h
    OPCODE/Ice/IceRay.cpp              
    OPCODE/Ice/IceRay.h              
    OPCODE/Ice/IceRevisitedRadix.cpp
    OPCODE/Ice/IceRevisitedRadix.h     
    OPCODE/Ice/IceSegment.cpp        
    OPCODE/Ice/IceSegment.h
    OPCODE/Ice/IceTriangle.cpp         
    OPCODE/Ice/IceTriangle.h         
    OPCODE/Ice/IceTriList.h
    OPCODE/Ice/IceTypes.h              
    OPCODE/Ice/IceUtils.cpp          
    OPCODE/Ice/IceUtils.h
)

set (joints_SOURCES 
    ode/src/joints/joints.h
    ode/src/joints/joint.h 
    ode/src/joints/joint.cpp
    ode/src/joints/joint_internal.h
    ode/src/joints/ball.h 
    ode/src/joints/ball.cpp
    ode/src/joints/hinge.h 
    ode/src/joints/hinge.cpp
    ode/src/joints/slider.h 
    ode/src/joints/slider.cpp
    ode/src/joints/contact.h 
    ode/src/joints/contact.cpp
    ode/src/joints/universal.h 
    ode/src/joints/universal.cpp
    ode/src/joints/hinge2.h 
    ode/src/joints/hinge2.cpp
    ode/src/joints/fixed.h 
    ode/src/joints/fixed.cpp
    ode/src/joints/null.h 
    ode/src/joints/null.cpp
    ode/src/joints/amotor.h 
    ode/src/joints/amotor.cpp
    ode/src/joints/lmotor.h 
    ode/src/joints/lmotor.cpp
    ode/src/joints/plane2d.h 
    ode/src/joints/plane2d.cpp
    ode/src/joints/pu.h 
    ode/src/joints/pu.cpp
    ode/src/joints/pr.h 
    ode/src/joints/pr.cpp
    ode/src/joints/piston.h 
    ode/src/joints/piston.cpp
)

# convenience library to simulate per object cflags
set (fast_SOURCES 
    ode/src/fastldlt.c 
    ode/src/fastltsolve.c 
    ode/src/fastdot.c 
    ode/src/fastlsolve.c
)    

set (libode_SOURCES 
    ode/src/array.cpp 
    ode/src/array.h
    ode/src/box.cpp
    ode/src/capsule.cpp
    ode/src/collision_cylinder_box.cpp
    ode/src/collision_cylinder_plane.cpp
    ode/src/collision_cylinder_sphere.cpp
    ode/src/collision_kernel.cpp
    ode/src/collision_kernel.h
    ode/src/collision_quadtreespace.cpp
    ode/src/collision_sapspace.cpp
    ode/src/collision_space.cpp
    ode/src/collision_space_internal.h
    ode/src/collision_std.h
    ode/src/collision_transform.cpp 
    ode/src/collision_transform.h
    ode/src/collision_trimesh_colliders.h
    ode/src/collision_trimesh_disabled.cpp
    ode/src/collision_trimesh_internal.h
    ode/src/collision_util.cpp 
    ode/src/collision_util.h
    ode/src/convex.cpp
    ode/src/cylinder.cpp
    ode/src/error.cpp
    ode/src/export-dif.cpp
    ode/src/heightfield.cpp 
    ode/src/heightfield.h
    ode/src/lcp.cpp 
    ode/src/lcp.h
    ode/src/mass.cpp
    ode/src/mat.cpp 
    ode/src/mat.h
    ode/src/matrix.cpp
    ode/src/memory.cpp
    ode/src/misc.cpp
    ode/src/objects.h
    ode/src/obstack.cpp 
    ode/src/obstack.h
    ode/src/ode.cpp
    ode/src/odeinit.cpp
    ode/src/odemath.cpp
    ode/src/odeou.h
    ode/src/odetls.h
    ode/src/plane.cpp
    ode/src/quickstep.cpp 
    ode/src/quickstep.h
    ode/src/ray.cpp
    ode/src/rotation.cpp
    ode/src/sphere.cpp
    ode/src/step.cpp 
    ode/src/step.h
    ode/src/stepfast.cpp
    ode/src/testing.cpp 
    ode/src/testing.h
    ode/src/timer.cpp
    ode/src/util.cpp 
    ode/src/util.h
)

###################################
#       O U    S T U F F
###################################


#if ENABLE_OU

#AM_CPPFLAGS += -I$(top_srcdir)/ou/include
#libode_la_LIBADD += $(top_builddir)/ou/src/ou/libou.la
#libode_la_SOURCES +=    odetls.cpp odetls.h
#                        odeou.cpp odeou.h

#endif


###################################
#   G I M P A C T    S T U F F
###################################

if (GIMPACT)
add_definitions(-DDdTRIMESH_ENABLED -DdTRIMESH_GIMPACT)
set (GIMPACT_SOURCES 
    ode/src/collision_trimesh_gimpact.cpp
    ode/src/collision_trimesh_trimesh.cpp
    ode/src/collision_trimesh_trimesh_new.cpp
    ode/src/collision_trimesh_sphere.cpp
    ode/src/collision_trimesh_ray.cpp
    ode/src/collision_trimesh_opcode.cpp
    ode/src/collision_trimesh_box.cpp
    ode/src/collision_trimesh_ccylinder.cpp
    ode/src/collision_trimesh_distance.cpp
    ode/src/collision_trimesh_internal.h
    ode/src/collision_cylinder_trimesh.cpp
    ode/src/collision_trimesh_plane.cpp
)
endif (GIMPACT)


#################################
#   O P C O D E    S T U F F
#################################

add_definitions(-DdTRIMESH_ENABLED -DdTRIMESH_OPCODE)

set (OPCODE_ODE_SOURCES   
    ode/src/collision_trimesh_trimesh.cpp
    ode/src/collision_trimesh_trimesh_new.cpp
    ode/src/collision_trimesh_sphere.cpp
    ode/src/collision_trimesh_ray.cpp
    ode/src/collision_trimesh_opcode.cpp
    ode/src/collision_trimesh_box.cpp
    ode/src/collision_trimesh_ccylinder.cpp
    ode/src/collision_trimesh_distance.cpp
    ode/src/collision_trimesh_internal.h
    ode/src/collision_cylinder_trimesh.cpp
    ode/src/collision_trimesh_plane.cpp
)

set (SOURCES
    ${joints_SOURCES}
    ${libode_SOURCES}
    ${OPCODE_ODE_SOURCES}
    ${GIMPACT_SOURCES}
    ${OPCODE_SOURCES}
    ${OPCODE_ICE_SOURCES}
    ${fast_SOURCES}
)

add_library(ode SHARED ${SOURCES})
target_link_libraries(ode)

set (libode_HEADERS 
	include/ode/collision_trimesh.h
    include/ode/mass.h
    include/ode/odecpp.h
    include/ode/common.h
    include/ode/matrix.h
    include/ode/odecpp_collision.h
    include/ode/compatibility.h
    include/ode/memory.h
    include/ode/contact.h
    include/ode/misc.h
    include/ode/odemath.h
    include/ode/odeinit.h
    include/ode/collision.h
    include/ode/error.h
    include/ode/objects.h
    include/ode/rotation.h
    include/ode/collision_space.h
    include/ode/export-dif.h
    include/ode/ode.h 
    include/ode/timer.h
    include/ode/odeconfig.h
)

install(TARGETS ode RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib )
install(FILES ${libode_HEADERS} DESTINATION include/ode)

