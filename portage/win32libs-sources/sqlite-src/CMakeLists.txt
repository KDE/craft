project( Sqlite )
cmake_minimum_required( VERSION 2.6 )

set ( sqlite_HEADER sqlite3.h sqlite3ext.h )

set ( libsqlite_SRC sqlite3.c  )
set( sqlite_SRC shell.c )

add_library ( libsqlite3 SHARED  ${libsqlite_SRC} )
set_target_properties(libsqlite3  PROPERTIES  OUTPUT_NAME "sqlite3")

install( TARGETS libsqlite3 RUNTIME DESTINATION bin LIBRARY DESTINATION lib ARCHIVE DESTINATION lib )

add_executable ( sqlite3 ${sqlite_SRC} )
target_link_libraries ( sqlite3 libsqlite3)

install( TARGETS sqlite3 RUNTIME DESTINATION bin LIBRARY DESTINATION lib ARCHIVE DESTINATION lib )

install( FILES ${sqlite_HEADER} DESTINATION include)